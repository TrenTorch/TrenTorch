"""
pytest data/app_data/01-numpy/08-random-sampling/02-seeding-and-reproducibility/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/08-random-sampling/{Path(__file__).resolve().parent.name}")
reproducible_draw = _module.reproducible_draw
draw_twice = _module.draw_twice
same_seed_same_output = _module.same_seed_same_output
skip_then_draw = _module.skip_then_draw


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
