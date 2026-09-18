"""
pytest data/app_data/05-transformers-llm/01-transformer-block/02-rmsnorm/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"05-transformers-llm/01-transformer-block/{Path(__file__).resolve().parent.name}")
rmsnorm_forward = _module.rmsnorm_forward

layer_norm_forward = load_solution("05-transformers-llm/01-transformer-block/01-layer-normalization-forward").layer_norm_forward


def test_matches_oracle_from_torch_nn_rmsnorm():
    # Values verified against torch.nn.RMSNorm(4, eps=1e-6) with matching weight.
    x = np.array(
        [
            [1.4940790731576061, -0.20515826376580087, 0.31306770165090136, -0.8540957393017248],
            [-2.5529898158340787, 0.6536185954403606, 0.8644361988595057, -0.7421650204064419],
        ]
    )
    gamma = np.array([2.2697546239876076, -1.4543656745987648, 0.04575851730144607, -0.1871838500258336])
    expected = np.array(
        [
            [3.8509829366657, 0.3388299041320479, 0.016267818209958512, 0.18154907185643146],
            [-4.036587393717138, -0.6621926911747296, 0.02755441888868035, 0.09677322733003796],
        ]
    )
    result = rmsnorm_forward(x, gamma)
    assert np.allclose(result, expected, atol=1e-6)


def test_output_shape_matches_input_shape():
    x = np.random.randn(3, 5, 8)
    gamma = np.ones(8)
    result = rmsnorm_forward(x, gamma)
    assert result.shape == x.shape


def test_with_gamma_one_root_mean_square_of_output_is_one():
    rng = np.random.RandomState(0)
    x = rng.randn(2, 16) * 5.0
    gamma = np.ones(16)
    result = rmsnorm_forward(x, gamma)
    rms_out = np.sqrt(np.mean(result**2, axis=-1))
    assert np.allclose(rms_out, 1.0, atol=1e-3)


def test_does_not_center_the_mean_unlike_layer_norm():
    # RMSNorm has no mean-subtraction step, so a constant-offset input
    # keeps a nonzero mean after normalization, unlike LayerNorm.
    x = np.array([[10.0, 11.0, 12.0, 13.0]])
    gamma = np.ones(4)
    result = rmsnorm_forward(x, gamma)
    assert not np.isclose(result.mean(), 0.0, atol=1e-2)


def test_rmsnorm_and_layer_norm_differ_on_a_shifted_input():
    # Directly targets a mutant that reimplements RMSNorm as LayerNorm
    # (subtracting the mean before scaling).
    x = np.array([[10.0, 11.0, 12.0, 13.0]])
    gamma = np.ones(4)
    beta = np.zeros(4)
    rms_result = rmsnorm_forward(x, gamma)
    ln_result = layer_norm_forward(x, gamma, beta)
    assert not np.allclose(rms_result, ln_result, atol=1e-2)


def test_scaling_input_by_a_constant_leaves_output_unchanged():
    # RMSNorm is scale-invariant: x and c*x normalize to the same output
    # (for c > 0), since both the numerator and the RMS denominator scale
    # by the same factor.
    rng = np.random.RandomState(2)
    x = rng.randn(2, 6)
    gamma = rng.randn(6)
    result_x = rmsnorm_forward(x, gamma)
    result_2x = rmsnorm_forward(2.0 * x, gamma)
    assert np.allclose(result_x, result_2x, atol=1e-4)


def test_uses_root_mean_square_not_plain_mean_of_squares_without_sqrt():
    # Directly targets a mutant that forgets the sqrt (dividing by the
    # mean of squares instead of its square root), which changes the
    # output's scale entirely.
    x = np.array([[3.0, 4.0]])  # mean of squares = 12.5, rms = sqrt(12.5)
    gamma = np.ones(2)
    result = rmsnorm_forward(x, gamma, eps=0.0)
    expected = x / np.sqrt(12.5)
    assert np.allclose(result, expected, atol=1e-6)
