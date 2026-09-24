"""
pytest data/app_data/01-numpy/08-random-sampling/05-assemble-reproducible-synthetic-dataset/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/08-random-sampling/{Path(__file__).resolve().parent.name}")
make_regression_dataset = _module.make_regression_dataset


def test_correct_shapes():
    result = make_regression_dataset(
        seed=0, n_samples=100, n_features=5, noise_std=0.1, test_fraction=0.3, hidden_units=8
    )
    assert result["X_train"].shape[1] == 5
    assert result["X_test"].shape[1] == 5
    assert result["y_train"].shape == (result["X_train"].shape[0],)
    assert result["y_test"].shape == (result["X_test"].shape[0],)
    assert result["true_w"].shape == (5,)
    assert result["W_init"].shape == (5, 8)
    assert len(result["y_train"]) + len(result["y_test"]) == 100


def test_same_seed_reproduces_everything():
    kwargs = dict(
        seed=1, n_samples=50, n_features=3, noise_std=0.2, test_fraction=0.2, hidden_units=4
    )
    a = make_regression_dataset(**kwargs)
    b = make_regression_dataset(**kwargs)
    for key in a:
        np.testing.assert_array_equal(a[key], b[key])


def test_different_seeds_differ():
    kwargs = dict(n_samples=50, n_features=3, noise_std=0.2, test_fraction=0.2, hidden_units=4)
    a = make_regression_dataset(seed=1, **kwargs)
    b = make_regression_dataset(seed=2, **kwargs)
    assert not np.array_equal(a["X_train"], b["X_train"])
    assert not np.array_equal(a["W_init"], b["W_init"])


def test_draw_order_matches_specification():
    seed, n_samples, n_features, hidden_units = 3, 20, 4, 6
    rng = np.random.default_rng(seed)
    expected_X = rng.standard_normal((n_samples, n_features))
    expected_true_w = rng.uniform(-1.0, 1.0, n_features)
    expected_noise = rng.normal(0.0, 0.5, n_samples)
    expected_split = rng.random(n_samples)
    expected_W_init = rng.normal(0.0, np.sqrt(2.0 / n_features), (n_features, hidden_units))
    expected_y = expected_X @ expected_true_w + expected_noise
    expected_is_test = expected_split < 0.25

    result = make_regression_dataset(
        seed=seed,
        n_samples=n_samples,
        n_features=n_features,
        noise_std=0.5,
        test_fraction=0.25,
        hidden_units=hidden_units,
    )

    np.testing.assert_array_equal(result["true_w"], expected_true_w)
    np.testing.assert_array_equal(result["W_init"], expected_W_init)
    np.testing.assert_array_equal(result["X_train"], expected_X[~expected_is_test])
    np.testing.assert_array_equal(result["y_train"], expected_y[~expected_is_test])
    np.testing.assert_array_equal(result["X_test"], expected_X[expected_is_test])
    np.testing.assert_array_equal(result["y_test"], expected_y[expected_is_test])


def test_targets_follow_linear_model_with_zero_noise():
    result = make_regression_dataset(
        seed=4, n_samples=30, n_features=3, noise_std=0.0, test_fraction=0.3, hidden_units=2
    )
    np.testing.assert_allclose(result["y_train"], result["X_train"] @ result["true_w"])
    np.testing.assert_allclose(result["y_test"], result["X_test"] @ result["true_w"])


def test_split_is_clean_partition_preserving_order():
    seed, n_samples, n_features = 5, 40, 3
    rng = np.random.default_rng(seed)
    expected_X = rng.standard_normal((n_samples, n_features))
    rng.uniform(-1.0, 1.0, n_features)
    rng.normal(0.0, 0.1, n_samples)
    expected_split = rng.random(n_samples)
    expected_is_test = expected_split < 0.4

    result = make_regression_dataset(
        seed=seed,
        n_samples=n_samples,
        n_features=n_features,
        noise_std=0.1,
        test_fraction=0.4,
        hidden_units=2,
    )
    reconstructed = np.empty_like(expected_X)
    reconstructed[~expected_is_test] = result["X_train"]
    reconstructed[expected_is_test] = result["X_test"]
    np.testing.assert_array_equal(reconstructed, expected_X)


def test_test_fraction_edge_cases():
    result_zero = make_regression_dataset(
        seed=6, n_samples=10, n_features=2, noise_std=0.1, test_fraction=0.0, hidden_units=3
    )
    assert result_zero["X_test"].shape == (0, 2)
    assert result_zero["X_train"].shape == (10, 2)

    result_one = make_regression_dataset(
        seed=6, n_samples=10, n_features=2, noise_std=0.1, test_fraction=1.0, hidden_units=3
    )
    assert result_one["X_train"].shape == (0, 2)
    assert result_one["X_test"].shape == (10, 2)


def test_weight_scale():
    n_features, hidden_units = 400, 300
    result = make_regression_dataset(
        seed=7,
        n_samples=10,
        n_features=n_features,
        noise_std=0.1,
        test_fraction=0.2,
        hidden_units=hidden_units,
    )
    expected_std = np.sqrt(2.0 / n_features)
    assert abs(result["W_init"].std() - expected_std) < 0.01
