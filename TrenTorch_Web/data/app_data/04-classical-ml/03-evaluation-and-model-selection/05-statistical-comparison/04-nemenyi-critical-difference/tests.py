"""
pytest tests.py
"""

import math

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
nemenyi_cd = _module.nemenyi_cd
significantly_different = _module.significantly_different


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_demsar_example_value():
    # k = 4, N = 10, q_0.05 = 2.569: CD = 2.569 * sqrt(20 / 60).
    assert np.isclose(nemenyi_cd(4, 10, 2.569), 2.569 * math.sqrt(20 / 60))


def test_cd_shrinks_with_more_datasets():
    assert nemenyi_cd(4, 40, 2.569) < nemenyi_cd(4, 10, 2.569)


def test_cd_grows_with_more_algorithms():
    assert nemenyi_cd(8, 10, 2.569) > nemenyi_cd(4, 10, 2.569)


def test_cd_scales_linearly_with_q_alpha():
    assert np.isclose(nemenyi_cd(5, 12, 4.0), 2 * nemenyi_cd(5, 12, 2.0))


def test_cd_doubles_when_datasets_shrink_fourfold():
    # CD scales as 1 / sqrt(n), so n = 16 -> n = 4 doubles it.
    assert np.isclose(nemenyi_cd(3, 4, 2.0), 2 * nemenyi_cd(3, 16, 2.0))


def test_cd_is_positive():
    assert nemenyi_cd(3, 5, 2.0) > 0


def test_gap_equal_to_cd_is_significant():
    cd = 1.5
    assert significantly_different(1.0, 2.5, cd)


def test_gap_below_cd_is_not_significant():
    assert not significantly_different(1.0, 2.4, 1.5)


def test_order_of_arguments_does_not_matter():
    assert significantly_different(4.0, 1.0, 2.0) == significantly_different(1.0, 4.0, 2.0)


def test_identical_ranks_are_never_significant_with_positive_cd():
    assert not significantly_different(2.0, 2.0, 0.1)


def test_zero_cd_makes_every_pair_significant():
    assert significantly_different(2.0, 2.0, 0.0)


def test_single_algorithm_raises():
    assert _raises_value_error(nemenyi_cd, 1, 10, 2.0)


def test_no_datasets_raises():
    assert _raises_value_error(nemenyi_cd, 4, 0, 2.0)


def test_nonpositive_q_raises():
    assert _raises_value_error(nemenyi_cd, 4, 10, 0.0)


def test_negative_cd_raises():
    assert _raises_value_error(significantly_different, 1.0, 2.0, -0.5)
