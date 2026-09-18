"""
pytest data/app_data/06-inference/02-kv-cache-and-decoding/01-rotary-position-embeddings-decoding/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

apply_rope = load_solution(
    f"06-inference/02-kv-cache-and-decoding/{Path(__file__).resolve().parent.name}"
).apply_rope


def test_position_zero_is_identity():
    x = np.array([1.0, 0.0, 1.0, 0.0])
    out = apply_rope(x, position=0)
    assert np.allclose(out, x)


def test_single_pair_position_one():
    out = apply_rope(np.array([1.0, 0.0]), position=1, base=10000.0)
    # theta_0 = 10000**0 = 1, so rotation angle is exactly 1 radian.
    assert np.allclose(out, [np.cos(1.0), np.sin(1.0)], atol=1e-6)


def test_rotation_preserves_pair_norm():
    rng = np.random.default_rng(0)
    x = rng.normal(size=8)
    out = apply_rope(x, position=7, base=10000.0)
    for i in range(0, 8, 2):
        assert np.isclose(x[i] ** 2 + x[i + 1] ** 2, out[i] ** 2 + out[i + 1] ** 2)


def test_batched_matches_per_row_single_calls():
    rng = np.random.default_rng(1)
    x = rng.normal(size=(4, 6))
    positions = [0, 1, 2, 3]
    batched = apply_rope(x, positions)
    for row in range(4):
        single = apply_rope(x[row], positions[row])
        assert np.allclose(batched[row], single)


def test_relative_position_property_dot_product():
    # Rotating both a "query" and a "key" vector must make their dot
    # product depend only on the DIFFERENCE of their positions.
    rng = np.random.default_rng(2)
    q, k = rng.normal(size=6), rng.normal(size=6)

    q_rot_a, k_rot_a = apply_rope(q, 5), apply_rope(k, 2)  # diff = 3
    q_rot_b, k_rot_b = apply_rope(q, 9), apply_rope(k, 6)  # diff = 3

    assert np.isclose(q_rot_a @ k_rot_a, q_rot_b @ k_rot_b, atol=1e-6)


def test_custom_base():
    out = apply_rope(np.array([2.0, 3.0]), position=5, base=100.0)
    theta = 100.0 ** 0
    angle = 5 * theta
    expected = [2.0 * np.cos(angle) - 3.0 * np.sin(angle), 2.0 * np.sin(angle) + 3.0 * np.cos(angle)]
    assert np.allclose(out, expected, atol=1e-6)
