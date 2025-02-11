from contextlib import contextmanager
from contextvars import ContextVar
from functools import wraps
from typing import Callable, Any, Coroutine, cast, Concatenate, Awaitable

import sqlalchemy.engine.url as SQURL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from Services.TemplateApiServise.WebApi.config import settings

Database = settings.database_config


url = SQURL.URL.create(
    drivername="postgresql+asyncpg",
    username=Database.user,
    password=Database.password,
    host=Database.host,
    port=Database.port,
    database=Database.database
)

engine = create_async_engine(url, pool_size=10, max_overflow=5)
factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


def require_session():
    session = db_session_var.get()
    assert session is not None, "Session context is not provided"
    return session


def transaction[SELF, **P, T]():
    def wrapper(
        cb: Callable[Concatenate[SELF, AsyncSession, P], Awaitable[T]],
    ) -> Callable[Concatenate[SELF, P], Coroutine[Any, Any, T]]:
        @wraps(cb)
        async def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
            if db_session_var.get() is not None:
                return await cb(*args, **kwargs)

            async with cast(AsyncSession, factory()) as session:
                with use_context_value(db_session_var, session):
                    result = await cb(*args, **kwargs)
                    await session.commit()
                    return result

        return wrapped

    return wrapper


@contextmanager
def use_context_value[T](context: ContextVar[T], value: T):
    reset = context.set(value)
    try:
        yield
    finally:
        context.reset(reset)


db_session_var: ContextVar[AsyncSession | None] = ContextVar(
    "db_session_var", default=None
)
