import time

import numpy as np


def time_function(fn, num_runs: int = 5) -> list:
    """
    Calls `fn()` (no arguments -- wrap anything that needs arguments in
    a lambda before passing it in) `num_runs` times, recording each
    call's wall-clock duration with `time.perf_counter()`. Returns the
    list of durations, one real, independent measurement per run
    (never a single averaged guess).
    """
    # TODO: loop num_runs times; each iteration, record
    # time.perf_counter() before and after calling fn(), append the
    # difference to a list, and return that list.
    pass


def benchmark_statistics(times: list) -> dict:
    """
    Summarizes a list of raw timing measurements (like time_function's
    output) into the standard descriptive statistics: mean, median,
    min, max, and standard deviation.
    """
    # TODO: convert times to a float array, return a dict with keys
    # "mean", "median", "min", "max", "std" computed via the matching
    # numpy functions.
    pass
