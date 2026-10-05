"""
pytest tests.py
"""

import numpy as np
from _load import load_solution

_module = load_solution(__file__)
create_rng = _module.create_rng
make_independent_rngs = _module.make_independent_rngs
draw = _module.draw
reproducible_draw = _module.reproducible_draw
draw_twice = _module.draw_twice
same_seed_same_output = _module.same_seed_same_output
skip_then_draw = _module.skip_then_draw


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


def test_same_seed_reproduces_exactly():
    np.testing.assert_array_equal(reproducible_draw(5, 4), reproducible_draw(5, 4))
    assert same_seed_same_output(5, 4) is True


def test_different_seeds_differ():
    assert not np.array_equal(reproducible_draw(1, 4), reproducible_draw(2, 4))


def test_state_advances_between_draws():
    first, second = draw_twice(7, 4)
    assert not np.array_equal(first, second)


def test_two_consecutive_draws_equal_one_long_draw():
    seed, n = 7, 4
    first, second = draw_twice(seed, n)
    combined = np.concatenate([first, second])
    np.testing.assert_array_equal(combined, reproducible_draw(seed, 2 * n))


def test_skip_then_draw_returns_correct_slice_of_sequence():
    seed, skip, n = 7, 3, 2
    rng = np.random.default_rng(seed)
    result = skip_then_draw(rng, skip, n)
    full_sequence = reproducible_draw(seed, skip + n)
    np.testing.assert_array_equal(result, full_sequence[skip : skip + n])


def test_callers_generator_is_mutated():
    seed = 7
    rng = np.random.default_rng(seed)
    skip_then_draw(rng, 3, 2)
    next_value = rng.random()
    reference_sequence = reproducible_draw(seed, 6)
    assert next_value == reference_sequence[5]
