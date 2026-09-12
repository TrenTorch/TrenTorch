"""
pytest data/app_data/05-transformers-llm/02-modern-transformer-architecture/08-rope-scaling/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"05-transformers-llm/02-modern-transformer-architecture/{Path(__file__).resolve().parent.name}"
)
compute_rope_angles_scaled = _module.compute_rope_angles_scaled

_rope_module = load_solution("04-seq-modeling/02-embeddings/06-rope")
compute_rope_angles = _rope_module.compute_rope_angles
apply_rope = _rope_module.apply_rope


def test_shape():
    angles = compute_rope_angles_scaled(seq_len=8, dim=4, scale_factor=2.0)
    assert angles.shape == (8, 2)


def test_scale_factor_one_reduces_to_unscaled_rope_angles():
    seq_len, dim = 10, 6
    scaled = compute_rope_angles_scaled(seq_len, dim, scale_factor=1.0)
    unscaled = compute_rope_angles(seq_len, dim)
    assert np.allclose(scaled, unscaled, atol=1e-10)


def test_extended_position_maps_onto_the_trained_range():
    # scale_factor = target_max_len / trained_max_len: position
    # target_max_len (the far end of the EXTENDED context) maps EXACTLY
    # to position trained_max_len (the far end of the ORIGINAL,
    # unscaled range), the defining property of this choice of
    # scale_factor.
    trained_max_len, target_max_len, dim = 100, 400, 8
    scale_factor = target_max_len / trained_max_len

    scaled_angles = compute_rope_angles_scaled(target_max_len + 1, dim, scale_factor)
    unscaled_angles = compute_rope_angles(trained_max_len + 1, dim)

    assert np.allclose(scaled_angles[target_max_len], unscaled_angles[trained_max_len], atol=1e-8)


def test_every_integer_multiple_of_scale_factor_maps_exactly_onto_an_unscaled_position():
    trained_max_len, dim, scale_factor = 50, 6, 4.0
    target_max_len = int(trained_max_len * scale_factor)
    scaled_angles = compute_rope_angles_scaled(target_max_len, dim, scale_factor)
    unscaled_angles = compute_rope_angles(trained_max_len, dim)

    for k in range(trained_max_len):
        scaled_position = int(k * scale_factor)
        assert np.allclose(scaled_angles[scaled_position], unscaled_angles[k], atol=1e-8)


def test_angles_are_strictly_smaller_than_unscaled_at_the_same_raw_position():
    seq_len, dim, scale_factor = 20, 8, 4.0
    scaled = compute_rope_angles_scaled(seq_len, dim, scale_factor)
    unscaled = compute_rope_angles(seq_len, dim)
    # Every scaled angle (position compressed by scale_factor > 1) must be
    # smaller than the corresponding unscaled angle, except at position 0.
    assert np.all(scaled[1:] < unscaled[1:])


def test_relative_position_dot_product_invariance_is_preserved_after_scaling():
    # Directly mirrors 04-seq-modeling/02-embeddings/06-rope's own
    # verification: the dot product between two rotated vectors should
    # depend only on their RELATIVE position offset, not their absolute
    # positions, even after position interpolation scaling.
    rng = np.random.RandomState(0)
    dim, scale_factor = 8, 3.0
    seq_len = 30
    angles = compute_rope_angles_scaled(seq_len, dim, scale_factor)

    x = rng.randn(dim)
    y = rng.randn(dim)

    # Two pairs with the SAME relative offset (5), at different absolute positions.
    x_rot_a = apply_rope(x, angles[2])
    y_rot_a = apply_rope(y, angles[7])
    dot_a = x_rot_a @ y_rot_a

    x_rot_b = apply_rope(x, angles[10])
    y_rot_b = apply_rope(y, angles[15])
    dot_b = x_rot_b @ y_rot_b

    assert np.isclose(dot_a, dot_b, atol=1e-6)


def test_larger_scale_factor_compresses_positions_more_aggressively():
    # Directly targets a mutant that multiplies by scale_factor instead
    # of dividing, which would EXPAND rather than COMPRESS the position
    # range, the opposite of what position interpolation needs.
    seq_len, dim = 20, 4
    angles_mild = compute_rope_angles_scaled(seq_len, dim, scale_factor=2.0)
    angles_aggressive = compute_rope_angles_scaled(seq_len, dim, scale_factor=8.0)
    assert np.all(angles_aggressive[1:] < angles_mild[1:])
