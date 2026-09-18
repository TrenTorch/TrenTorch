"""
pytest data/app_data/03-dl-training/05-why-deep-networks-work/04-batchnorm/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/05-why-deep-networks-work/{Path(__file__).resolve().parent.name}")
batchnorm_forward = _module.batchnorm_forward


def test_training_mode_output_has_zero_mean_and_unit_variance_before_gamma_beta():
    x = np.random.randn(100, 3) * 5 + 10
    gamma = np.ones(3)
    beta = np.zeros(3)
    out, _, _ = batchnorm_forward(x, gamma, beta, np.zeros(3), np.ones(3), training=True)
    assert np.allclose(out.mean(axis=0), 0.0, atol=1e-6)
    assert np.allclose(out.var(axis=0), 1.0, atol=1e-3)


def test_gamma_and_beta_are_applied_after_normalization():
    x = np.random.randn(50, 2)
    gamma = np.array([2.0, 3.0])
    beta = np.array([1.0, -1.0])
    out, _, _ = batchnorm_forward(x, gamma, beta, np.zeros(2), np.ones(2), training=True)
    assert np.allclose(out.mean(axis=0), beta, atol=1e-6)
    assert np.allclose(out.std(axis=0), gamma, atol=1e-2)


def test_matches_known_oracle_from_pytorch_batchnorm1d_training_mode():
    # verified directly against torch.nn.BatchNorm1d(4) with a fixed seed
    x = np.array(
        [
            [1.0, 2.0, 3.0, 4.0],
            [2.0, 3.0, 4.0, 5.0],
            [3.0, 4.0, 5.0, 6.0],
            [4.0, 5.0, 6.0, 7.0],
        ]
    )
    gamma = np.ones(4)
    beta = np.zeros(4)
    out, running_mean, running_var = batchnorm_forward(
        x, gamma, beta, np.zeros(4), np.ones(4), momentum=0.1, eps=1e-5, training=True
    )
    # batch mean per column: [2.5, 3.5, 4.5, 5.5]; each column has the same variance (1.25)
    expected_out_col0 = (x[:, 0] - 2.5) / np.sqrt(1.25 + 1e-5)
    assert np.allclose(out[:, 0], expected_out_col0, atol=1e-5)
    assert np.allclose(running_mean, np.array([0.25, 0.35, 0.45, 0.55]), atol=1e-5)


def test_running_var_update_uses_unbiased_variance_not_biased():
    x = np.array([[1.0], [3.0]])  # mean=2, biased var=1.0, unbiased var=2.0 (n=2)
    gamma = np.array([1.0])
    beta = np.array([0.0])
    _, _, running_var = batchnorm_forward(
        x, gamma, beta, np.zeros(1), np.zeros(1), momentum=1.0, eps=1e-5, training=True
    )
    # momentum=1.0 means running_var becomes exactly the (unbiased) batch variance
    assert np.isclose(running_var[0], 2.0)


def test_eval_mode_uses_running_stats_not_batch_stats():
    x = np.array([[100.0], [200.0]])  # batch stats would be wildly different
    gamma = np.array([1.0])
    beta = np.array([0.0])
    running_mean = np.array([0.0])
    running_var = np.array([1.0])
    out, rm_after, rv_after = batchnorm_forward(
        x, gamma, beta, running_mean, running_var, eps=1e-5, training=False
    )
    expected = (x - 0.0) / np.sqrt(1.0 + 1e-5)
    assert np.allclose(out, expected)


def test_eval_mode_does_not_modify_running_stats():
    x = np.random.randn(10, 3)
    gamma = np.ones(3)
    beta = np.zeros(3)
    running_mean = np.array([1.0, 2.0, 3.0])
    running_var = np.array([4.0, 5.0, 6.0])
    _, rm_after, rv_after = batchnorm_forward(
        x, gamma, beta, running_mean.copy(), running_var.copy(), training=False
    )
    assert np.allclose(rm_after, running_mean)
    assert np.allclose(rv_after, running_var)


def test_training_mode_updates_running_mean_toward_the_batch_mean():
    x = np.ones((10, 2)) * 5.0  # batch mean = [5, 5]
    gamma = np.ones(2)
    beta = np.zeros(2)
    running_mean = np.zeros(2)
    _, rm_after, _ = batchnorm_forward(
        x, gamma, beta, running_mean, np.ones(2), momentum=0.1, training=True
    )
    # running_mean should move PARTWAY from 0 toward 5, not jump all the way
    assert 0.0 < rm_after[0] < 5.0


def test_training_normalization_uses_biased_variance_not_unbiased():
    # Directly targets a mutant that uses the UNBIASED variance for the
    # actual normalization step (ddof=1) instead of the biased variance
    # (ddof=0) that torch.nn.BatchNorm1d's forward pass actually uses:
    # this changes the normalized output's scale measurably for a small
    # batch.
    x = np.array([[1.0], [2.0], [3.0], [4.0]])  # n=4
    gamma = np.array([1.0])
    beta = np.array([0.0])
    out, _, _ = batchnorm_forward(x, gamma, beta, np.zeros(1), np.ones(1), eps=0.0, training=True)
    biased_var = x.var(axis=0, ddof=0)  # 1.25
    expected = (x - x.mean(axis=0)) / np.sqrt(biased_var)
    assert np.allclose(out, expected, atol=1e-6)
