"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
normalized_expected_cost = _module.normalized_expected_cost


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_equal_costs_and_balanced_prior_average_the_rates():
    # PC = 0.5, so NEC = (0.2 + 0.4) / 2 = 0.3.
    assert np.isclose(normalized_expected_cost(0.2, 0.4, 0.5, 1.0, 1.0), 0.3)


def test_perfect_classifier_has_zero_cost():
    assert normalized_expected_cost(0.0, 0.0, 0.3, 5.0, 1.0) == 0.0


def test_always_positive_classifier_costs_one_minus_pc():
    # fnr = 0, fpr = 1: NEC = 1 - PC. With p = 0.5 and C_FN = 3, C_FP = 1, PC = 0.75.
    assert np.isclose(normalized_expected_cost(0.0, 1.0, 0.5, 3.0, 1.0), 0.25)


def test_always_negative_classifier_costs_pc():
    # fnr = 1, fpr = 0: NEC = PC = 0.75 in the same setting.
    assert np.isclose(normalized_expected_cost(1.0, 0.0, 0.5, 3.0, 1.0), 0.75)


def test_nec_is_between_zero_and_one_on_grid():
    for fnr in np.linspace(0, 1, 5):
        for fpr in np.linspace(0, 1, 5):
            v = normalized_expected_cost(fnr, fpr, 0.2, 4.0, 1.0)
            assert 0.0 <= v <= 1.0 + 1e-12


def test_higher_fnr_with_expensive_fn_increases_cost():
    low = normalized_expected_cost(0.1, 0.1, 0.2, 10.0, 1.0)
    high = normalized_expected_cost(0.3, 0.1, 0.2, 10.0, 1.0)
    assert high > low


def test_scaling_both_costs_leaves_nec_unchanged():
    a = normalized_expected_cost(0.2, 0.3, 0.4, 2.0, 5.0)
    b = normalized_expected_cost(0.2, 0.3, 0.4, 20.0, 50.0)
    assert np.isclose(a, b)


def test_rare_positive_class_with_costly_fn_weights_fnr_heavily():
    # PC = 0.01 * 100 / (1 + 0.99) is about 0.5, so a classifier that misses every positive costs about 0.5.
    v = normalized_expected_cost(1.0, 0.0, 0.01, 100.0, 1.0)
    assert v > 0.4


def test_prior_shift_changes_weight_on_fnr():
    a = normalized_expected_cost(0.5, 0.0, 0.1, 1.0, 1.0)
    b = normalized_expected_cost(0.5, 0.0, 0.9, 1.0, 1.0)
    assert a < b


def test_rates_outside_unit_interval_raise():
    assert _raises_value_error(normalized_expected_cost, 1.2, 0.0, 0.5, 1.0, 1.0)


def test_prior_at_boundary_raises():
    assert _raises_value_error(normalized_expected_cost, 0.1, 0.1, 0.0, 1.0, 1.0)
    assert _raises_value_error(normalized_expected_cost, 0.1, 0.1, 1.0, 1.0, 1.0)


def test_nonpositive_cost_raises():
    assert _raises_value_error(normalized_expected_cost, 0.1, 0.1, 0.5, 0.0, 1.0)
    assert _raises_value_error(normalized_expected_cost, 0.1, 0.1, 0.5, 1.0, -1.0)
