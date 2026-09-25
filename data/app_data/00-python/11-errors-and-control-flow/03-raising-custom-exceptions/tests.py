"""
pytest data/app_data/00-python/11-errors-and-control-flow/03-raising-custom-exceptions/tests.py
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-python/11-errors-and-control-flow/{Path(__file__).resolve().parent.name}"
)
InsufficientFundsError = _module.InsufficientFundsError
withdraw = _module.withdraw
parse_positive_int = _module.parse_positive_int
log_and_reraise = _module.log_and_reraise
check_sorted = _module.check_sorted


def test_insufficient_funds_error_message_and_attributes():
    e = InsufficientFundsError(100, 150)
    assert str(e) == "balance 100 is less than 150"
    assert e.balance == 100
    assert e.requested == 150
    assert isinstance(e, Exception)


def test_withdraw_chooses_right_exception():
    assert withdraw(100, 50) == 50
    assert withdraw(100, 100) == 0
    with pytest.raises(InsufficientFundsError):
        withdraw(100, 150)
    with pytest.raises(ValueError):
        withdraw(100, 0)
    with pytest.raises(ValueError):
        withdraw(100, -5)


def test_parse_positive_int_chaining():
    try:
        parse_positive_int("x")
        assert False, "expected ValueError"
    except ValueError as e:
        assert isinstance(e.__cause__, ValueError)

    try:
        parse_positive_int("-5")
        assert False, "expected ValueError"
    except ValueError as e:
        assert e.__cause__ is None


def test_log_and_reraise_preserves_exception():
    log = []
    original = ValueError("boom")

    def failing():
        raise original

    try:
        log_and_reraise(failing, log)
        assert False, "expected ValueError"
    except ValueError as e:
        assert e is original
    assert log == ["boom"]

    log2 = []
    assert log_and_reraise(lambda: 42, log2) == 42
    assert log2 == []


def test_check_sorted_assertion_behavior():
    check_sorted([1, 2, 3])
    check_sorted([1])
    check_sorted([])
    with pytest.raises(AssertionError, match="not sorted"):
        check_sorted([2, 1])
