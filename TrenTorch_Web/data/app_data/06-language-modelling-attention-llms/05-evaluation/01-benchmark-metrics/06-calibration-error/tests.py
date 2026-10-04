"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
expected_calibration_error = _module.expected_calibration_error
brier_score = _module.brier_score


def test_1_overconfident_model_hand_computed():
    conf = np.full(10, 0.9)
    correct = np.array([1] * 5 + [0] * 5)
    assert np.isclose(expected_calibration_error(conf, correct), 0.4)


def test_2_perfectly_calibrated_bin_has_zero_error():
    conf = np.full(10, 0.7)
    correct = np.array([1] * 7 + [0] * 3)
    assert np.isclose(expected_calibration_error(conf, correct), 0.0)


def test_3_bins_are_weighted_by_size():
    conf = np.array([0.95] * 8 + [0.15] * 2)
    correct = np.array([1] * 8 + [1, 1])
    # bin (0.9, 1.0]: gap 0.05 weight 0.8 ; bin (0.1, 0.2]: gap 0.85 weight 0.2
    assert np.isclose(expected_calibration_error(conf, correct), 0.8 * 0.05 + 0.2 * 0.85)


def test_4_upper_bin_edge_is_inclusive():
    # confidence exactly 0.5 with 10 bins belongs to (0.4, 0.5]
    conf = np.array([0.5, 0.6])
    correct = np.array([1, 0])
    # bins are separate: gaps 0.5 and 0.6, weights 1/2 each
    assert np.isclose(expected_calibration_error(conf, correct), 0.5 * 0.5 + 0.5 * 0.6)
    both = expected_calibration_error(np.array([0.5, 0.5]), np.array([1, 0]))
    assert np.isclose(both, 0.0)


def test_5_zero_confidence_goes_in_the_first_bin():
    assert np.isclose(expected_calibration_error(np.array([0.0]), np.array([0])), 0.0)


def test_6_brier_hand_computed():
    assert np.isclose(brier_score([0.8, 0.3], [1, 0]), (0.04 + 0.09) / 2)


def test_7_matches_naive_loop_and_inputs_untouched():
    rng = np.random.RandomState(0)
    conf = rng.uniform(0.05, 1.0, 200)
    corr = (rng.uniform(size=200) < conf * 0.8).astype(int)
    s1, s2 = conf.copy(), corr.copy()
    total = 0.0
    for b in range(10):
        lo, hi = b / 10, (b + 1) / 10
        sel = (conf > lo) & (conf <= hi)
        if sel.any():
            total += sel.mean() * abs(corr[sel].mean() - conf[sel].mean())
    assert np.isclose(expected_calibration_error(conf, corr, 10), total)
    assert np.array_equal(conf, s1) and np.array_equal(corr, s2)
