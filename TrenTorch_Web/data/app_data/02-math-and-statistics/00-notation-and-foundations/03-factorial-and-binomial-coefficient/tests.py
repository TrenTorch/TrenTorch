"""
pytest data/app_data/02-math-and-statistics/00-notation-and-foundations/03-factorial-and-binomial-coefficient/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    "02-math-and-statistics/00-notation-and-foundations/03-factorial-and-binomial-coefficient"
)
factorial = _module.factorial
n_choose_k = _module.n_choose_k


# ---- 1-2: basic correctness ----


def test_1_factorial_of_5():
    assert factorial(5) == 120


def test_2_5_choose_2():
    assert n_choose_k(5, 2) == 10


# ---- shape / general-case coverage ----


def test_3_factorial_of_several_values():
    assert factorial(1) == 1
    assert factorial(3) == 6
    assert factorial(6) == 720


def test_4_n_choose_k_returns_an_int_not_a_float():
    result = n_choose_k(6, 3)
    assert isinstance(result, int)
    assert result == 20


# ---- edge cases ----


def test_5_factorial_of_zero_is_one():
    assert factorial(0) == 1


def test_6_choose_zero_is_always_one():
    assert n_choose_k(7, 0) == 1


def test_7_choose_n_is_always_one():
    assert n_choose_k(7, 7) == 1


def test_8_choose_one_equals_n():
    assert n_choose_k(9, 1) == 9


# ---- mutation-catching ----


def test_9_factorial_does_not_include_zero_as_a_factor():
    # A wrong implementation starting the loop at 0 (range(0, n+1)) would
    # multiply by 0 and always return 0 for n >= 1.
    assert factorial(4) == 24


def test_10_binomial_coefficient_is_symmetric():
    # C(n, k) == C(n, n-k) always -- a wrong denominator ordering would
    # break this for asymmetric n/k.
    assert n_choose_k(8, 3) == n_choose_k(8, 5)


def test_11_pascals_rule_holds():
    # C(n, k) == C(n-1, k-1) + C(n-1, k) -- catches a formula typo that
    # happens to be right only at the symmetric edge cases above.
    n, k = 7, 3
    assert n_choose_k(n, k) == n_choose_k(n - 1, k - 1) + n_choose_k(n - 1, k)


# ---- independent oracle ----


def test_12_matches_hand_computed_reference_values():
    # Computed independently: 10! = 3628800, C(10, 4) = 210.
    assert factorial(10) == 3628800
    assert n_choose_k(10, 4) == 210
