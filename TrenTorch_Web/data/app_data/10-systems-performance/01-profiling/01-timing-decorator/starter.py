import time
from functools import wraps
from typing import Callable


def timed(func: Callable) -> Callable:
    """
    func: any callable

    Returns a wrapped version of func that, when called, runs func with
    whatever arguments it was given and returns (result, elapsed_seconds)
    instead of just result.
    """
    # TODO: use functools.wraps(func) on your inner wrapper function (so
    # the wrapped function keeps func's real __name__/docstring), record
    # time.perf_counter() before and after calling func(*args, **kwargs),
    # and return (result, elapsed_seconds).
    pass
