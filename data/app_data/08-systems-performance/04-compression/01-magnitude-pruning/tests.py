"""
pytest data/app_data/08-systems-performance/04-compression/01-magnitude-pruning/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

magnitude_prune = load_solution(f"08-systems-performance/04-compression/{Path(__file__).resolve().parent.name}").magnitude_prune


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_zero_sparsity_leaves_the_weight_unchanged():
    w = np.array([1.0, -2.0, 3.0])
    result = magnitude_prune(w, 0.0)
    assert np.array_equal(result, w)


def test_02_prunes_exactly_the_smallest_magnitude_fraction():
    w = np.array([1.0, -0.1, 5.0, -0.2, 3.0])  # 2 smallest by |.|: -0.1, -0.2
    result = magnitude_prune(w, sparsity=0.4)
    assert result[1] == 0.0
    assert result[3] == 0.0
    assert result[0] == 1.0 and result[2] == 5.0 and result[4] == 3.0


# --- Shape / general-case coverage -----------------------------------


def test_03_higher_sparsity_prunes_more_elements():
    rng = np.random.default_rng(0)
    w = rng.normal(size=100)
    low = magnitude_prune(w, 0.1)
    high = magnitude_prune(w, 0.9)
    assert np.count_nonzero(low) > np.count_nonzero(high)


def test_04_works_on_a_2d_weight_matrix():
    w = np.array([[1.0, -0.1], [5.0, -0.2]])
    result = magnitude_prune(w, 0.5)
    assert result.shape == (2, 2)
    assert np.count_nonzero(result) == 2


# --- Parameter handling -------------------------------------------------


def test_05_full_sparsity_prunes_almost_everything():
    rng = np.random.default_rng(1)
    w = rng.normal(size=10)
    result = magnitude_prune(w, sparsity=0.9)
    assert np.count_nonzero(result) <= 1


def test_06_larger_magnitude_weights_always_survive_pruning():
    w = np.array([0.01, 0.02, 100.0, -100.0])
    result = magnitude_prune(w, sparsity=0.5)
    assert result[2] == 100.0
    assert result[3] == -100.0


# --- Edge cases ---------------------------------------------------------


def test_07_sparsity_zero_or_negative_prunes_nothing():
    w = np.array([1.0, -2.0])
    assert np.array_equal(magnitude_prune(w, 0.0), w)
    assert np.array_equal(magnitude_prune(w, -0.5), w)


def test_08_single_element_array():
    w = np.array([5.0])
    result = magnitude_prune(w, 0.9)
    assert result.shape == (1,)


# --- Array hygiene ------------------------------------------------------


def test_09_does_not_mutate_its_input():
    w = np.array([1.0, -0.1, 5.0])
    w_copy = w.copy()
    magnitude_prune(w, 0.5)
    assert np.array_equal(w, w_copy)


# --- Independent correctness oracle -----------------------------------


def test_10_matches_real_pytorch_l1_unstructured_pruning_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    #
    # Generated once, offline, with:
    #   torch.manual_seed(0)
    #   w = torch.randn(2, 5)
    #   lin = torch.nn.Linear(5, 2, bias=False)
    #   lin.weight = torch.nn.Parameter(w.clone())
    #   torch.nn.utils.prune.l1_unstructured(lin, name="weight", amount=0.4)
    #   lin.weight  # baked below
    #
    # This test needs no torch installed to run.
    w = np.array(
        [
            [1.5410, -0.2934, -2.1788, 0.5684, -1.0845],
            [-1.3986, 0.4033, 0.8380, -0.7193, -0.4033],
        ]
    )
    expected = np.array(
        [
            [1.5410, -0.0, -2.1788, 0.0, -1.0845],
            [-1.3986, 0.0, 0.8380, -0.7193, -0.0],
        ]
    )
    result = magnitude_prune(w, sparsity=0.4)
    assert np.allclose(result, expected)
