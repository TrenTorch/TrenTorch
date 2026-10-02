"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
create_rng = _module.create_rng
make_independent_rngs = _module.make_independent_rngs
draw = _module.draw


def test_returns_genuine_generator():
    rng = create_rng(42)
    assert isinstance(rng, np.random.Generator)


def test_same_seed_gives_same_first_draw():
    rng_a = create_rng(42)
    rng_b = create_rng(42)
    np.testing.assert_array_equal(draw(rng_a, 5), draw(rng_b, 5))


def test_independence_of_two_generators():
    rng_a, rng_b = make_independent_rngs(1, 2)
    draw(rng_a, 10)
    expected = np.random.default_rng(2).random(3)
    np.testing.assert_array_equal(draw(rng_b, 3), expected)


def test_does_not_touch_legacy_global_state():
    np.random.seed(0)
    expected = np.random.rand()

    np.random.seed(0)
    create_rng(99)
    draw(create_rng(99), 5)
    actual = np.random.rand()

    assert actual == expected


def test_draw_returns_correct_shape_and_range():
    rng = create_rng(0)
    result = draw(rng, 100)
    assert result.shape == (100,)
    assert np.all(result >= 0) and np.all(result < 1)
