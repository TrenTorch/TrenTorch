"""
pytest data/app_data/01-numpy/08-random-sampling/03-uniform-and-integer-arrays/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/08-random-sampling/{Path(__file__).resolve().parent.name}")
uniform_array = _module.uniform_array
random_integers = _module.random_integers
roll_dice = _module.roll_dice


def test_correct_shape_including_multidimensional():
    rng = np.random.default_rng(0)
    assert uniform_array(rng, 0, 1, (5,)).shape == (5,)
    assert uniform_array(rng, 0, 1, (2, 3)).shape == (2, 3)
    assert random_integers(rng, 0, 10, (4, 2)).shape == (4, 2)


def test_uniform_values_stay_within_bounds():
    rng = np.random.default_rng(0)
    result = uniform_array(rng, -5.0, -1.0, (10000,))
    assert np.all(result >= -5.0) and np.all(result < -1.0)


def test_uniform_covers_the_range():
    rng = np.random.default_rng(0)
    result = uniform_array(rng, 0.0, 10.0, (50000,))
    assert result.min() < 0.5
    assert result.max() > 9.5


def test_integer_upper_bound_is_exclusive():
    rng = np.random.default_rng(0)
    result = random_integers(rng, 0, 3, (10000,))
    values = set(result.tolist())
    assert values == {0, 1, 2}
    assert 3 not in values


def test_roll_dice_includes_top_face():
    rng = np.random.default_rng(0)
    result = roll_dice(rng, 10000, 6)
    values = set(result.tolist())
    assert 1 in values and 6 in values
    assert 0 not in values and 7 not in values


def test_correct_dtype_kind():
    rng = np.random.default_rng(0)
    assert np.issubdtype(uniform_array(rng, 0, 1, (5,)).dtype, np.floating)
    assert np.issubdtype(random_integers(rng, 0, 10, (5,)).dtype, np.integer)


def test_seed_controlled():
    rng_a = np.random.default_rng(0)
    rng_b = np.random.default_rng(0)
    np.testing.assert_array_equal(
        uniform_array(rng_a, 0, 1, (5,)), uniform_array(rng_b, 0, 1, (5,))
    )
