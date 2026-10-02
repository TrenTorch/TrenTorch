"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
detect_outliers_iqr = _module.detect_outliers_iqr
detect_outliers_zscore = _module.detect_outliers_zscore


def test_iqr_flags_an_obvious_outlier():
    x = np.array([10.0, 12.0, 11.0, 13.0, 12.0, 11.0, 10.0, 100.0])
    result = detect_outliers_iqr(x)
    assert result[-1]  # the 100.0
    assert not result[:-1].any()


def test_iqr_flags_nothing_in_tightly_clustered_data():
    x = np.array([10.0, 10.5, 11.0, 10.2, 9.8, 10.3])
    result = detect_outliers_iqr(x)
    assert not result.any()


def test_iqr_smaller_k_flags_more_points():
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 20.0])
    strict = detect_outliers_iqr(x, k=0.5)
    lenient = detect_outliers_iqr(x, k=3.0)
    assert strict.sum() >= lenient.sum()


def test_zscore_flags_an_obvious_outlier_in_a_larger_sample():
    rng = np.random.default_rng(0)
    x = np.concatenate([rng.normal(0.0, 1.0, size=100), [50.0]])
    result = detect_outliers_zscore(x)
    assert result[-1]


def test_zscore_flags_nothing_in_tightly_clustered_data():
    x = np.array([10.0, 10.5, 11.0, 10.2, 9.8, 10.3])
    result = detect_outliers_zscore(x)
    assert not result.any()


def test_zscore_higher_threshold_flags_fewer_points():
    rng = np.random.default_rng(1)
    x = rng.normal(0.0, 1.0, size=200)
    lenient = detect_outliers_zscore(x, threshold=1.0)
    strict = detect_outliers_zscore(x, threshold=4.0)
    assert lenient.sum() >= strict.sum()


def test_iqr_uses_percentile_bounds_not_a_fixed_multiple_of_mean():
    # Directly targets a mutant that flags based on distance from the
    # mean instead of the IQR-based bounds (e.g. |x - mean| > some
    # constant). Skewed data can make these two rules disagree sharply.
    x = np.array([10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 50.0])  # one clear high outlier
    result = detect_outliers_iqr(x)
    assert result[-1]
    assert result.sum() == 1


def test_outlier_masks_are_boolean_and_correct_shape():
    x = np.array([1.0, 2.0, 3.0, 100.0])
    iqr_result = detect_outliers_iqr(x)
    z_result = detect_outliers_zscore(x)
    assert iqr_result.dtype == bool
    assert z_result.dtype == bool
    assert iqr_result.shape == x.shape
    assert z_result.shape == x.shape
