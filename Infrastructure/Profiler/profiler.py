import inspect
import pathlib
from collections.abc import Callable
from typing import Any, cast

from line_profiler import LineProfiler

from config import settings

FULL_PATH = pathlib.Path(__file__).parent.resolve()


def profiler[F](prefixname: str = "") -> Callable[[F], F]:
    def decorator(func: F) -> F:
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            if settings.app_config.environment != "local":
                return await func(*args, **kwargs)

            line_profiler = LineProfiler()

            line_profiler.add_function(func)
            line_profiler.enable()
            try:
                if inspect.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)
            finally:
                line_profiler.disable()

                with open(f"{FULL_PATH}/{prefixname}{func.__name__}_profiler_result.txt", "a") as f:  # NOSONAR
                    line_profiler.print_stats(stream=f)
                    f.seek(0)
                    f.close()

        return cast(F, wrapper)

    return decorator
