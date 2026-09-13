"""
pytest data/app_data/08-systems-performance/01-profiling/01-timing-decorator/tests.py
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

timed = load_solution(f"08-systems-performance/01-profiling/{Path(__file__).resolve().parent.name}").timed


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_returns_a_tuple_of_result_and_elapsed():
    @timed
    def add(a, b):
        return a + b

    result, elapsed = add(2, 3)
    assert result == 5
    assert isinstance(elapsed, float)


def test_02_elapsed_is_never_negative():
    @timed
    def noop():
        return None

    _, elapsed = noop()
    assert elapsed >= 0.0


# --- Shape / general-case coverage -----------------------------------


def test_03_elapsed_reflects_actual_sleep_duration():
    @timed
    def sleep_a_bit():
        time.sleep(0.05)
        return "done"

    result, elapsed = sleep_a_bit()
    assert result == "done"
    assert elapsed >= 0.05


def test_04_faster_function_reports_smaller_elapsed_than_slower_one():
    @timed
    def fast():
        return 1

    @timed
    def slow():
        time.sleep(0.05)
        return 1

    _, fast_elapsed = fast()
    _, slow_elapsed = slow()
    assert slow_elapsed > fast_elapsed


# --- Parameter handling -------------------------------------------------


def test_05_positional_and_keyword_arguments_both_pass_through():
    @timed
    def combine(a, b, c=0):
        return a + b + c

    result, _ = combine(1, 2, c=3)
    assert result == 6


# --- Edge cases ---------------------------------------------------------


def test_06_works_on_a_function_with_no_arguments_and_no_return_value():
    @timed
    def side_effect_only():
        pass

    result, elapsed = side_effect_only()
    assert result is None
    assert elapsed >= 0.0


def test_07_preserves_the_wrapped_functions_name_and_docstring():
    @timed
    def documented_function():
        """A real docstring."""
        return 1

    assert documented_function.__name__ == "documented_function"
    assert documented_function.__doc__ == "A real docstring."


# --- Array hygiene / decorator hygiene -----------------------------------


def test_08_can_be_applied_to_multiple_different_functions_independently():
    @timed
    def f():
        return "f"

    @timed
    def g():
        return "g"

    result_f, _ = f()
    result_g, _ = g()
    assert result_f == "f"
    assert result_g == "g"


# --- Independent correctness oracle -----------------------------------


def test_09_matches_a_manual_perf_counter_measurement_within_tolerance():
    @timed
    def sleep_100ms():
        time.sleep(0.1)

    manual_start = time.perf_counter()
    _, wrapped_elapsed = sleep_100ms()
    manual_elapsed = time.perf_counter() - manual_start

    # The wrapper's own measurement should be very close to (and never
    # larger than) a measurement taken around the whole call from outside.
    assert wrapped_elapsed <= manual_elapsed + 1e-3
    assert abs(wrapped_elapsed - manual_elapsed) < 0.05
