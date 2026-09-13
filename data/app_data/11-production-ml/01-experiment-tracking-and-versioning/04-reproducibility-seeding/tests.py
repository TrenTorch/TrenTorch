"""
pytest data/app_data/11-production-ml/01-experiment-tracking-and-versioning/04-reproducibility-seeding/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"11-production-ml/01-experiment-tracking-and-versioning/{Path(__file__).resolve().parent.name}")
seeded_numpy_sequence = _module.seeded_numpy_sequence
seeded_python_random_sequence = _module.seeded_python_random_sequence
capture_reproducibility_config = _module.capture_reproducibility_config
verify_reproducible = _module.verify_reproducible


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_same_seed_gives_identical_numpy_sequences():
    a = seeded_numpy_sequence(42, 5)
    b = seeded_numpy_sequence(42, 5)
    assert np.array_equal(a, b)


def test_02_different_seeds_give_different_sequences():
    a = seeded_numpy_sequence(1, 5)
    b = seeded_numpy_sequence(2, 5)
    assert not np.array_equal(a, b)


# --- General-case coverage --------------------------------------------


def test_03_python_random_and_numpy_are_genuinely_separate_sources():
    # Pinning ONE source of randomness has zero effect on the other --
    # a real, common reproducibility gotcha.
    py_seq_a = seeded_python_random_sequence(7, 5)
    np_seq = seeded_numpy_sequence(999, 5)  # unrelated seed, unrelated generator
    py_seq_b = seeded_python_random_sequence(7, 5)
    assert py_seq_a == py_seq_b  # unaffected by the numpy call in between


def test_04_seeded_python_sequence_reproducible():
    a = seeded_python_random_sequence(10, 4)
    b = seeded_python_random_sequence(10, 4)
    assert a == b


def test_05_capture_reproducibility_config_bundles_both_seeds():
    config = capture_reproducibility_config(numpy_seed=42, python_seed=7)
    assert config == {"numpy_seed": 42, "python_random_seed": 7}


# --- Parameter handling -------------------------------------------------


def test_06_verify_reproducible_true_for_a_genuinely_seeded_function():
    assert verify_reproducible(lambda seed: seeded_numpy_sequence(seed, 5), seed=3, num_trials=4) is True


def test_07_verify_reproducible_false_for_a_genuinely_unseeded_function():
    import random as _random

    def unseeded(seed):
        return [_random.random()]  # ignores the seed entirely

    assert verify_reproducible(unseeded, seed=3, num_trials=5) is False


# --- Edge cases ---------------------------------------------------------


def test_08_sequence_length_matches_requested_n():
    assert len(seeded_numpy_sequence(1, 10)) == 10
    assert len(seeded_python_random_sequence(1, 10)) == 10


def test_09_single_trial_is_trivially_reproducible():
    assert verify_reproducible(lambda seed: seeded_numpy_sequence(seed, 3), seed=1, num_trials=1) is True


# --- Independent correctness oracle -----------------------------------


def test_10_verify_reproducible_actually_calls_fn_multiple_times():
    # Directly targets a mutant that always returns True without
    # genuinely calling fn more than once (or without comparing the
    # results at all) -- count real calls via a closure and confirm
    # the reported trial count matches what was actually executed.
    call_count = {"n": 0}

    def counting_fn(seed):
        call_count["n"] += 1
        return seeded_numpy_sequence(seed, 3)

    verify_reproducible(counting_fn, seed=5, num_trials=6)
    assert call_count["n"] == 6
