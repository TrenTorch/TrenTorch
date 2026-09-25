"""
pytest data/app_data/00-python/11-errors-and-control-flow/02-try-except-else-finally/tests.py
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-python/11-errors-and-control-flow/{Path(__file__).resolve().parent.name}"
)
safe_int = _module.safe_int
parse_pair = _module.parse_pair
run_steps = _module.run_steps
count_convertible = _module.count_convertible
cleanup_return = _module.cleanup_return


def test_safe_int_handles_both_exception_types():
    assert safe_int("42", 0) == 42
    assert safe_int("x", -1) == -1
    assert safe_int(None, -1) == -1
    assert safe_int("", -1) == -1
    assert safe_int("3.5", -1) == -1


def test_parse_pair_failure_modes():
    assert parse_pair("3:4") == (3, 4)
    assert parse_pair("3") is None
    assert parse_pair("3:4:5") is None
    assert parse_pair("a:4") is None
    assert parse_pair("3:") is None
    assert parse_pair(" 3 : 4 ") == (3, 4)


def test_run_steps_order_for_both_outcomes():
    log = []
    run_steps(log, False)
    assert log == ["try", "else", "finally"]

    log2 = []
    run_steps(log2, True)
    assert log2 == ["try", "except", "finally"]


def test_count_convertible_with_mixed_types():
    assert count_convertible(["1", "x", None, 3.9, "07"]) == 3
    assert count_convertible([]) == 0


def test_finally_runs_even_on_early_return():
    log = []
    assert cleanup_return(log, True) == "early"
    assert log == ["cleanup"]

    log2 = []
    assert cleanup_return(log2, False) == "end"
    assert log2 == ["cleanup"]


def test_exceptions_are_not_over_caught():
    class Weird:
        def __int__(self):
            raise RuntimeError("nope")

    with pytest.raises(RuntimeError):
        safe_int(Weird(), 0)
