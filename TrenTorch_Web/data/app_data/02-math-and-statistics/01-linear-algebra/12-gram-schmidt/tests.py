"""
pytest data/app_data/02-math-and-statistics/01-linear-algebra/12-gram-schmidt/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

gram_schmidt = load_solution(
    "02-math-and-statistics/01-linear-algebra/12-gram-schmidt"
).gram_schmidt


# ---- 1-2: basic correctness ----


def test_1_two_vectors_produce_unit_length_output():
    vectors = [np.array([3.0, 1.0]), np.array([2.0, 2.0])]
    basis = gram_schmidt(vectors)
    for u in basis:
        assert np.isclose(np.linalg.norm(u), 1.0, atol=1e-10)


def test_2_two_vectors_produce_orthogonal_output():
    vectors = [np.array([3.0, 1.0]), np.array([2.0, 2.0])]
    basis = gram_schmidt(vectors)
    assert np.isclose(basis[0] @ basis[1], 0.0, atol=1e-10)


# ---- shape / general-case coverage ----


def test_3_first_vector_keeps_its_original_direction():
    vectors = [np.array([3.0, 4.0]), np.array([1.0, 0.0])]
    basis = gram_schmidt(vectors)
    # First basis vector must be a positive scalar multiple of the input.
    ratio = basis[0] / vectors[0]
    np.testing.assert_allclose(ratio, [ratio[0], ratio[0]], atol=1e-10)
    assert ratio[0] > 0


def test_4_three_vectors_all_mutually_orthonormal():
    vectors = [
        np.array([1.0, 1.0, 0.0]),
        np.array([1.0, 0.0, 1.0]),
        np.array([0.0, 1.0, 1.0]),
    ]
    basis = gram_schmidt(vectors)
    for i in range(3):
        assert np.isclose(np.linalg.norm(basis[i]), 1.0, atol=1e-10)
        for j in range(i + 1, 3):
            assert np.isclose(basis[i] @ basis[j], 0.0, atol=1e-10)


def test_5_basis_spans_the_same_space():
    vectors = [np.array([2.0, 0.0]), np.array([1.0, 3.0])]
    basis = gram_schmidt(vectors)
    # Every original vector should be exactly reconstructible as a
    # combination of the resulting basis.
    M = np.column_stack(basis)
    for v in vectors:
        coeffs = np.linalg.solve(M, v)
        np.testing.assert_allclose(M @ coeffs, v, atol=1e-10)


# ---- edge cases ----


def test_6_already_orthonormal_input_is_unchanged():
    vectors = [np.array([1.0, 0.0]), np.array([0.0, 1.0])]
    basis = gram_schmidt(vectors)
    np.testing.assert_allclose(basis[0], [1.0, 0.0], atol=1e-10)
    np.testing.assert_allclose(basis[1], [0.0, 1.0], atol=1e-10)


def test_7_single_vector_is_just_normalized():
    vectors = [np.array([3.0, 4.0])]
    basis = gram_schmidt(vectors)
    np.testing.assert_allclose(basis[0], [0.6, 0.8], atol=1e-10)


def test_8_input_vectors_are_not_mutated():
    vectors = [np.array([3.0, 1.0]), np.array([2.0, 2.0])]
    originals = [v.copy() for v in vectors]
    gram_schmidt(vectors)
    for v, original in zip(vectors, originals):
        np.testing.assert_array_equal(v, original)


# ---- mutation-catching ----


def test_9_subtracts_against_every_earlier_vector_not_just_the_last():
    # With 3+ vectors, a wrong implementation that only subtracts the
    # MOST RECENT basis vector's projection (not every earlier one)
    # would fail to be orthogonal to earlier basis vectors.
    vectors = [
        np.array([1.0, 0.0, 0.0]),
        np.array([1.0, 1.0, 0.0]),
        np.array([1.0, 1.0, 1.0]),
    ]
    basis = gram_schmidt(vectors)
    assert np.isclose(basis[2] @ basis[0], 0.0, atol=1e-10)
    assert np.isclose(basis[2] @ basis[1], 0.0, atol=1e-10)


def test_10_normalization_happens_after_all_subtractions_not_before():
    # A wrong implementation normalizing too early would still produce
    # SOME unit vector, but it would not be orthogonal to the earlier
    # basis vectors after the (now-rescaled) projection subtraction.
    vectors = [
        np.array([2.0, 0.0]),
        np.array([1.0, 3.0]),
    ]
    basis = gram_schmidt(vectors)
    assert np.isclose(basis[0] @ basis[1], 0.0, atol=1e-10)
    assert np.isclose(np.linalg.norm(basis[1]), 1.0, atol=1e-10)


# ---- independent oracle ----


def test_11_matches_a_hand_computed_reference_case():
    # v1=[3,1], v2=[2,2]. u1 = [3,1]/sqrt(10).
    # proj of v2 onto u1: (v2.v1/v1.v1)*v1 = (8/10)*[3,1] = [2.4, 0.8]
    # w2 = [2,2]-[2.4,0.8] = [-0.4, 1.2], norm = sqrt(0.16+1.44)=sqrt(1.6)
    vectors = [np.array([3.0, 1.0]), np.array([2.0, 2.0])]
    basis = gram_schmidt(vectors)
    np.testing.assert_allclose(basis[0], np.array([3.0, 1.0]) / np.sqrt(10), atol=1e-10)
    expected_u2 = np.array([-0.4, 1.2]) / np.sqrt(1.6)
    np.testing.assert_allclose(basis[1], expected_u2, atol=1e-10)
