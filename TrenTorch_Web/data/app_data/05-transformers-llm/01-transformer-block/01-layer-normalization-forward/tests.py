"""
pytest data/app_data/05-transformers-llm/01-transformer-block/01-layer-normalization-forward/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"05-transformers-llm/01-transformer-block/{Path(__file__).resolve().parent.name}")
layer_norm_forward = _module.layer_norm_forward


def test_matches_oracle_from_torch_nn_layernorm():
    # Values verified against torch.nn.LayerNorm(4, eps=1e-5) with matching weight/bias.
    x = np.array(
        [
            [1.764052345967664, 0.4001572083672233, 0.9787379841057392, 2.240893199201458],
            [1.8675579901499675, -0.977277879876411, 0.9500884175255894, -0.1513572082976979],
        ]
    )
    gamma = np.array([-0.10321885179355784, 0.41059850193837233, 0.144043571160878, 1.454273506962975])
    beta = np.array([0.7610377251469934, 0.12167501649282841, 0.44386323274542566, 0.33367432737426683])
    expected = np.array(
        [
            [0.7000856460231688, -0.4268235690867649, 0.36915296657592617, 2.1718799813652927],
            [0.6227524183736523, -0.4109937761863005, 0.514340654534904, -0.4395763264590258],
        ]
    )
    result = layer_norm_forward(x, gamma, beta)
    assert np.allclose(result, expected, atol=1e-8)


def test_with_gamma_one_beta_zero_output_has_zero_mean_and_unit_variance_per_row():
    rng = np.random.RandomState(0)
    x = rng.randn(2, 4)
    gamma = np.ones(4)
    beta = np.zeros(4)
    result = layer_norm_forward(x, gamma, beta)
    assert np.allclose(result.mean(axis=-1), 0.0, atol=1e-6)
    assert np.allclose(result.var(axis=-1), 1.0, atol=1e-4)


def test_output_shape_matches_input_shape():
    x = np.random.randn(3, 5, 8)
    gamma = np.ones(8)
    beta = np.zeros(8)
    result = layer_norm_forward(x, gamma, beta)
    assert result.shape == x.shape


def test_normalizes_along_last_axis_only_not_globally():
    # Two rows with wildly different scales; each row must be normalized
    # independently, not against the whole array's mean/variance.
    x = np.array([[1.0, 2.0, 3.0, 4.0], [100.0, 200.0, 300.0, 400.0]])
    gamma = np.ones(4)
    beta = np.zeros(4)
    result = layer_norm_forward(x, gamma, beta)
    assert np.allclose(result[0], result[1], atol=1e-4)


def test_uniform_row_stays_near_zero_thanks_to_eps():
    # A constant row has variance 0; without eps this would divide by zero.
    x = np.array([[5.0, 5.0, 5.0, 5.0]])
    gamma = np.ones(4)
    beta = np.zeros(4)
    result = layer_norm_forward(x, gamma, beta)
    assert np.all(np.isfinite(result))
    assert np.allclose(result, 0.0, atol=1e-2)


def test_uses_biased_variance_not_bessel_corrected():
    # Directly targets a mutant that uses ddof=1 (sample variance) instead
    # of the population variance (ddof=0) PyTorch's LayerNorm actually uses,
    # which silently produces the wrong scale for every row.
    x = np.array([[1.0, 2.0, 3.0, 4.0]])
    gamma = np.ones(4)
    beta = np.zeros(4)
    result = layer_norm_forward(x, gamma, beta)
    biased_var = np.var(x, axis=-1, ddof=0)
    manual = (x - x.mean(axis=-1, keepdims=True)) / np.sqrt(biased_var + 1e-5)
    assert np.allclose(result, manual, atol=1e-8)


def test_gamma_and_beta_are_applied_after_normalization():
    # Directly targets a mutant that applies gamma/beta before normalizing
    # (or forgets one of them), which would change the output's scale/shift.
    x = np.random.RandomState(1).randn(2, 4)
    gamma = np.array([2.0, 2.0, 2.0, 2.0])
    beta = np.array([10.0, 10.0, 10.0, 10.0])
    result = layer_norm_forward(x, gamma, beta)
    baseline = layer_norm_forward(x, np.ones(4), np.zeros(4))
    assert np.allclose(result, 2.0 * baseline + 10.0, atol=1e-6)
