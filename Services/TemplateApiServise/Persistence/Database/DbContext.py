from contextlib import contextmanager
from contextvars import ContextVar, Token
from functools import wraps
from typing import Callable, Any, Coroutine, Generator, Concatenate, Awaitable

import sqlalchemy.engine.url as SQURL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from config import DatabaseConfig, settings

Database: DatabaseConfig = settings.database_config


url: SQURL.URL = SQURL.URL.create(
    drivername="postgresql+asyncpg",
    username=Database.user,
    password=Database.password,
    host=Database.host,
    port=Database.port,
    database=Database.database
)

engine: AsyncEngine = create_async_engine(url=url, pool_size=10, max_overflow=5)
factory: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


def require_session() -> AsyncSession:
    session: AsyncSession | None = db_session_var.get()
    assert session is not None, "Session context is not provided"
    return session


def transaction[SELF, **P, T](cb: Callable[Concatenate[SELF, AsyncSession, P], Awaitable[T]]) -> Callable[Concatenate[SELF, P], Coroutine[Any, Any, T]]:
    @wraps(wrapped=cb)
    async def wrapped(self: SELF, *args: P.args, **kwargs: P.kwargs) -> T:
        session: AsyncSession | None = db_session_var.get()
        if session is not None:
            return await cb(self, session, *args, **kwargs)

        async with factory() as session:
            with use_context_value(context=db_session_var, value=session):
                result: T = await cb(self, session, *args, **kwargs)
                # await session.commit()
                return result

    return wrapped


@contextmanager
def use_context_value[T](context: ContextVar[T], value: T) -> Generator[None, Any, None]:
    reset: Token[T] = context.set(value)
    try:
        yield
    finally:
        context.reset(reset)


db_session_var: ContextVar[AsyncSession | None] = ContextVar(
    "db_session_var", default=None
)
