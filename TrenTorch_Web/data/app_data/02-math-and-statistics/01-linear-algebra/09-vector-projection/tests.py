"""
pytest data/app_data/02-math-and-statistics/01-linear-algebra/09-vector-projection/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution("02-math-and-statistics/01-linear-algebra/09-vector-projection")
project = _module.project
orthogonal_component = _module.orthogonal_component


# ---- 1-2: basic correctness ----


def test_1_project_onto_axis_aligned_vector():
    a = np.array([3.0, 4.0])
    b = np.array([1.0, 0.0])
    np.testing.assert_allclose(project(a, b), [3.0, 0.0])


def test_2_orthogonal_component_of_axis_aligned_case():
    a = np.array([3.0, 4.0])
    b = np.array([1.0, 0.0])
    np.testing.assert_allclose(orthogonal_component(a, b), [0.0, 4.0])


# ---- shape / general-case coverage ----


def test_3_project_onto_non_axis_aligned_vector():
    a = np.array([2.0, 2.0])
    b = np.array([1.0, 0.0])
    result = project(a, b)
    np.testing.assert_allclose(result, [2.0, 0.0])


def test_4_higher_dimensional_vectors():
    a = np.array([1.0, 2.0, 3.0])
    b = np.array([1.0, 1.0, 1.0])
    result = project(a, b)
    expected_scalar = (1 + 2 + 3) / 3
    np.testing.assert_allclose(result, expected_scalar * b)


# ---- edge cases ----


def test_5_vector_already_parallel_to_b():
    a = np.array([2.0, 4.0])
    b = np.array([1.0, 2.0])
    np.testing.assert_allclose(project(a, b), a)
    np.testing.assert_allclose(orthogonal_component(a, b), [0.0, 0.0], atol=1e-10)


def test_6_vector_already_perpendicular_to_b():
    a = np.array([0.0, 5.0])
    b = np.array([1.0, 0.0])
    np.testing.assert_allclose(project(a, b), [0.0, 0.0])
    np.testing.assert_allclose(orthogonal_component(a, b), a)


def test_7_negative_components():
    a = np.array([-3.0, -4.0])
    b = np.array([1.0, 0.0])
    np.testing.assert_allclose(project(a, b), [-3.0, 0.0])


# ---- mutation-catching ----


def test_8_reconstruction_identity_holds():
    # project(a, b) + orthogonal_component(a, b) must exactly reconstruct
    # a -- catches any implementation that gets one function's formula
    # slightly wrong even if it looks right in isolation.
    a = np.array([5.0, -2.0, 3.0])
    b = np.array([1.0, 1.0, 2.0])
    reconstructed = project(a, b) + orthogonal_component(a, b)
    np.testing.assert_allclose(reconstructed, a, atol=1e-10)


def test_9_orthogonal_component_is_genuinely_perpendicular_to_b():
    # A wrong implementation (e.g. forgetting to divide by b . b) would
    # not actually produce a component with zero dot product against b.
    a = np.array([4.0, 1.0, -2.0])
    b = np.array([2.0, 3.0, 1.0])
    orth = orthogonal_component(a, b)
    assert np.isclose(orth @ b, 0.0, atol=1e-10)


def test_10_projection_scale_uses_b_dot_b_not_norm_of_b():
    # A common off-by-formula mistake is dividing by ||b|| instead of
    # b . b (||b||^2) -- this only coincides when ||b|| == 1.
    a = np.array([6.0, 0.0])
    b = np.array([2.0, 0.0])  # ||b|| = 2, b.b = 4
    np.testing.assert_allclose(project(a, b), [6.0, 0.0])


# ---- independent oracle ----


def test_11_matches_a_hand_computed_reference_case():
    a = np.array([3.0, 1.0])
    b = np.array([1.0, 2.0])
    # scalar = (3*1 + 1*2) / (1*1 + 2*2) = 5/5 = 1
    np.testing.assert_allclose(project(a, b), [1.0, 2.0])
    np.testing.assert_allclose(orthogonal_component(a, b), [2.0, -1.0])
