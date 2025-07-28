import pathlib
from functools import wraps

from line_profiler import LineProfiler

FULL_PATH = pathlib.Path(__file__).parent.resolve()


class Profiler:
    def __init__(self, filename=f"{FULL_PATH}/profile_results.txt"):
        self.filename = filename
        self.profiler = LineProfiler()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.profiler.add_function(func)
            self.profiler.enable()

            result = func(*args, **kwargs)

            self.profiler.disable()
            with open(self.filename, "a") as f:
                self.profiler.print_stats(stream=f)

            return result

        return wrapper
