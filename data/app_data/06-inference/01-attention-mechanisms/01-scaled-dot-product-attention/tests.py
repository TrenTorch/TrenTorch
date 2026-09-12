"""
pytest data/app_data/06-inference/01-attention-mechanisms/01-scaled-dot-product-attention/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

scaled_dot_product_attention = load_solution(
    f"06-inference/01-attention-mechanisms/{Path(__file__).resolve().parent.name}"
).scaled_dot_product_attention


def test_unmasked_two_key_example():
    output, weights = scaled_dot_product_attention(
        Q=np.array([[1.0, 0.0]]),
        K=np.array([[1.0, 0.0], [0.0, 1.0]]),
        V=np.array([[10.0, 0.0], [0.0, 10.0]]),
    )
    # scores = [1, 0] / sqrt(2) = [0.7071, 0] -> softmax = [0.6698, 0.3302]
    assert np.allclose(weights, [[0.6698, 0.3302]], atol=1e-3)
    assert np.allclose(output, [[6.698, 3.302]], atol=1e-2)


def test_masked_forces_all_weight_onto_unmasked_key():
    output, _ = scaled_dot_product_attention(
        Q=np.array([[1.0, 1.0]]),
        K=np.array([[1.0, 1.0], [1.0, 1.0]]),
        V=np.array([[1.0, 0.0], [0.0, 1.0]]),
        mask=np.array([[1, 0]]),
    )
    assert np.allclose(output, [[1.0, 0.0]])


def test_uniform_attention_when_keys_identical():
    _, weights = scaled_dot_product_attention(
        Q=np.array([[0.0, 0.0]]),
        K=np.array([[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]]),
        V=np.array([[2.0, 0.0], [0.0, 2.0], [4.0, 4.0]]),
    )
    assert np.allclose(weights, [[1 / 3, 1 / 3, 1 / 3]])


def test_rows_of_weights_sum_to_one():
    rng = np.random.default_rng(0)
    Q, K, V = rng.normal(size=(5, 4)), rng.normal(size=(6, 4)), rng.normal(size=(6, 3))
    _, weights = scaled_dot_product_attention(Q, K, V)
    assert np.allclose(weights.sum(axis=-1), 1.0)


def test_causal_3x3_mask_matches_hand_computation():
    Q = K = V = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    mask = np.array([[1, 0, 0], [1, 1, 0], [1, 1, 1]])
    output, weights = scaled_dot_product_attention(Q, K, V, mask=mask)
    # Row 0 can only see key 0 -> weight is exactly [1, 0, 0].
    assert np.allclose(weights[0], [1.0, 0.0, 0.0])
    assert np.allclose(output[0], V[0])


def test_no_overflow_or_nan_for_large_score_magnitudes():
    Q = np.array([[100.0, 0.0]])
    K = np.array([[100.0, 0.0], [-100.0, 0.0]])
    V = np.array([[1.0, 0.0], [0.0, 1.0]])
    output, weights = scaled_dot_product_attention(Q, K, V)
    assert np.all(np.isfinite(output))
    assert np.all(np.isfinite(weights))
    assert np.allclose(weights[0], [1.0, 0.0], atol=1e-6)
