import sys
from collections.abc import Callable
from typing import Any, cast

from loguru import logger

from config import LogLevelEnum

logger_format = """
<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> |
<level>{level: <8}</level> |
<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>
"""


def setup_logging(log_level: LogLevelEnum = LogLevelEnum.INFO) -> None:
    logger.remove()

    logger.add(
        sink=sys.stderr,
        format=logger_format,
        level=log_level,
        colorize=True,
    )


def log[F](operation_name: str) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger.debug(f"Starting {operation_name}", operation=operation_name)
            try:
                result = await func(*args, **kwargs)  # type: ignore
                return result  # type: ignore
            except Exception as e:
                logger.error(
                    f"Failed {operation_name}",
                    operation=operation_name,
                    error=str(e),
                    exc_info=True,
                )
                raise

        return cast(F, wrapper)

    return decorator
