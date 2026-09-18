"""
pytest data/app_data/05-transformers-llm/02-modern-transformer-architecture/10-logit-scaling/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"05-transformers-llm/02-modern-transformer-architecture/{Path(__file__).resolve().parent.name}"
)
scale_logits_before_softmax = _module.scale_logits_before_softmax

softmax_last_axis = load_solution("04-seq-modeling/04-attention/03-softmax-last-axis").softmax_last_axis


def _entropy(p):
    return -np.sum(p * np.log(p + 1e-12), axis=-1)


def test_output_shape_matches_input_shape():
    logits = np.random.randn(5, 20)
    result = scale_logits_before_softmax(logits, d_model=64)
    assert result.shape == logits.shape


def test_scales_by_exactly_one_over_sqrt_d_model():
    logits = np.array([4.0, -2.0, 6.0])
    result = scale_logits_before_softmax(logits, d_model=16)
    assert np.allclose(result, logits / 4.0, atol=1e-10)


def test_scaling_is_linear_doubling_logits_doubles_the_scaled_result():
    logits = np.array([1.0, 2.0, 3.0])
    result_a = scale_logits_before_softmax(logits, d_model=64)
    result_b = scale_logits_before_softmax(2.0 * logits, d_model=64)
    assert np.allclose(result_b, 2.0 * result_a, atol=1e-10)


def test_larger_d_model_produces_a_smaller_scaled_magnitude_for_the_same_raw_logits():
    logits = np.array([10.0, -5.0, 3.0])
    result_small = scale_logits_before_softmax(logits, d_model=16)
    result_large = scale_logits_before_softmax(logits, d_model=256)
    assert np.all(np.abs(result_large) < np.abs(result_small))


def test_scaling_keeps_softmax_entropy_roughly_stable_as_d_model_grows():
    # Simulate raw logits whose magnitude grows with sqrt(d_model), as
    # real dot-product-based logits naturally would (mirroring
    # 01-scaled-dot-product-attention's own motivation for the analogous
    # 1/sqrt(d_k) scaling). Without scaling, softmax collapses toward a
    # one-hot distribution (entropy -> 0) as d_model grows; with scaling,
    # entropy stays roughly constant.
    rng = np.random.RandomState(0)
    vocab_size = 50
    base_logits = rng.randn(vocab_size)

    entropies_unscaled = []
    for d_model in [16, 64, 256, 1024]:
        raw_logits = base_logits * np.sqrt(d_model)
        entropies_unscaled.append(_entropy(softmax_last_axis(raw_logits)))

    # Unscaled entropy should shrink (monotonically, in this construction)
    # as d_model grows: softmax gets sharper and sharper.
    assert entropies_unscaled == sorted(entropies_unscaled, reverse=True)
    assert entropies_unscaled[0] > 2.0 * entropies_unscaled[-1]

    # At the largest d_model, scaling should recover a much higher-entropy
    # (closer to uniform) distribution than the unscaled version gives.
    d_model = 1024
    raw_logits = base_logits * np.sqrt(d_model)
    scaled_logits = scale_logits_before_softmax(raw_logits, d_model)
    unscaled_entropy = _entropy(softmax_last_axis(raw_logits))
    scaled_entropy = _entropy(softmax_last_axis(scaled_logits))
    assert scaled_entropy > 3.0 * unscaled_entropy


def test_uses_sqrt_of_d_model_not_d_model_itself():
    # Directly targets a mutant that divides by d_model instead of
    # sqrt(d_model), an easy off-by-a-square-root error.
    logits = np.array([9.0])
    result = scale_logits_before_softmax(logits, d_model=9)
    assert np.isclose(result[0], 3.0, atol=1e-10)  # 9 / sqrt(9) = 3, not 9 / 9 = 1
