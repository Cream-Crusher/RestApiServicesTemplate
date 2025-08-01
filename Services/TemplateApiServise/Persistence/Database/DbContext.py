from collections.abc import Awaitable, Callable, Coroutine, Generator
from contextlib import contextmanager
from contextvars import ContextVar, Token
from functools import wraps
from typing import Any, Concatenate, cast

import sqlalchemy.engine.url as SQURL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from config import DatabaseConfig, settings

Database: DatabaseConfig = settings.database_config


url: SQURL.URL = SQURL.URL.create(
    drivername="postgresql+asyncpg",
    username=Database.user,
    password=Database.password,
    host=Database.host,
    port=Database.port,
    database=Database.database,
)

engine: AsyncEngine = create_async_engine(url=url, pool_size=10, max_overflow=5)
factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


def get_session() -> AsyncSession:
    session: AsyncSession | None = db_session_var.get()
    assert session is not None, "Session context is not provided"
    return session


def transaction[SELF, **P, T]():  # type: ignore
    def wrapper(
        cb: Callable[[Concatenate[SELF, AsyncSession, P]], Awaitable[T]],  # type: ignore
    ) -> Callable[[Concatenate[SELF, P]], Coroutine[Any, Any, T]]:  # type: ignore
        @wraps(cb)
        async def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
            if db_session_var.get() is not None:
                return await cb(*args, **kwargs)  # type: ignore

            async with cast(AsyncSession, factory()) as session:  # type: ignore
                with use_context_value(db_session_var, session):  # type: ignore
                    result = await cb(*args, **kwargs)  # type: ignore
                    await session.commit()  # type: ignore
                    return result  # type: ignore

        return wrapped  # type: ignore

    return wrapper


@contextmanager
def use_context_value[T](context: ContextVar[T], value: T) -> Generator[None, Any, None]:
    reset: Token[T] = context.set(value)
    try:
        yield
    finally:
        context.reset(reset)


db_session_var: ContextVar[AsyncSession | None] = ContextVar("db_session_var", default=None)
