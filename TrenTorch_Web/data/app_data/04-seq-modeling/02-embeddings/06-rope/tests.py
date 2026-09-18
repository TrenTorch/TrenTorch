"""
pytest data/app_data/04-seq-modeling/02-embeddings/06-rope/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"04-seq-modeling/02-embeddings/{Path(__file__).resolve().parent.name}")
compute_rope_angles = _module.compute_rope_angles
apply_rope = _module.apply_rope


def test_compute_rope_angles_shape():
    angles = compute_rope_angles(seq_len=10, dim=8)
    assert angles.shape == (10, 4)


def test_compute_rope_angles_position_zero_is_all_zeros():
    angles = compute_rope_angles(seq_len=5, dim=6)
    assert np.allclose(angles[0], 0.0)


def test_apply_rope_at_angle_zero_leaves_x_unchanged():
    x = np.array([1.0, 2.0, 3.0, 4.0])
    angles = np.zeros(2)
    result = apply_rope(x, angles)
    assert np.allclose(result, x)


def test_apply_rope_matches_hand_computed_90_degree_rotation():
    # A 90-degree rotation of (1, 0) should give (0, 1)
    x = np.array([1.0, 0.0])
    angles = np.array([np.pi / 2])
    result = apply_rope(x, angles)
    assert np.allclose(result, [0.0, 1.0], atol=1e-10)


def test_apply_rope_preserves_the_norm_of_each_pair():
    x = np.array([3.0, 4.0, 1.0, 2.0])  # two pairs: (3,4) norm=5, (1,2) norm=sqrt(5)
    angles = np.array([0.7, 1.3])
    result = apply_rope(x, angles)
    original_norms = np.sqrt(x[0::2] ** 2 + x[1::2] ** 2)
    result_norms = np.sqrt(result[0::2] ** 2 + result[1::2] ** 2)
    assert np.allclose(original_norms, result_norms)


def test_apply_rope_output_shape_matches_input():
    x = np.random.randn(3, 5, 8)  # (batch, seq_len, dim)
    angles = compute_rope_angles(seq_len=5, dim=8)
    result = apply_rope(x, angles)
    assert result.shape == x.shape


def test_dot_product_depends_only_on_relative_position_not_absolute():
    np.random.seed(0)
    dim, seq_len = 8, 20
    q = np.random.randn(dim)
    k = np.random.randn(dim)
    angles = compute_rope_angles(seq_len, dim)

    def dot_at(m, n):
        return apply_rope(q, angles[m]) @ apply_rope(k, angles[n])

    # same relative offset (3), different absolute positions: must match
    assert np.isclose(dot_at(5, 2), dot_at(10, 7))
    assert np.isclose(dot_at(5, 2), dot_at(15, 12))


def test_dot_product_differs_for_different_relative_offsets():
    np.random.seed(1)
    dim, seq_len = 8, 20
    q = np.random.randn(dim)
    k = np.random.randn(dim)
    angles = compute_rope_angles(seq_len, dim)
    dot_offset_3 = apply_rope(q, angles[5]) @ apply_rope(k, angles[2])
    dot_offset_10 = apply_rope(q, angles[10]) @ apply_rope(k, angles[0])
    assert not np.isclose(dot_offset_3, dot_offset_10)


def test_rotation_uses_the_correct_sign_convention_not_a_flipped_rotation():
    # Directly targets a mutant that swaps the sign convention
    # (x1*sin + x2*cos for the FIRST output, x1*cos - x2*sin for the
    # SECOND, i.e. a clockwise rotation instead of counterclockwise, or
    # equivalently negating the angle): for a 90-degree rotation of
    # (1, 0), a flipped-sign implementation gives (0, -1) instead of the
    # correct (0, 1).
    x = np.array([1.0, 0.0])
    angles = np.array([np.pi / 2])
    result = apply_rope(x, angles)
    assert np.isclose(result[1], 1.0, atol=1e-10)
    assert not np.isclose(result[1], -1.0, atol=1e-10)
