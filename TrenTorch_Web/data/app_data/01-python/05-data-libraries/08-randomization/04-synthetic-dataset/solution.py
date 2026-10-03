import numpy as np


def make_regression_dataset(
    seed: int,
    n_samples: int,
    n_features: int,
    noise_std: float,
    test_fraction: float,
    hidden_units: int,
) -> dict:
    rng = np.random.default_rng(seed)

    X = rng.standard_normal((n_samples, n_features))
    true_w = rng.uniform(-1.0, 1.0, n_features)
    noise = rng.normal(0.0, noise_std, n_samples)
    split = rng.random(n_samples)
    W_init = rng.normal(0.0, np.sqrt(2.0 / n_features), (n_features, hidden_units))

    y = X @ true_w + noise

    is_test = split < test_fraction

    return {
        "X_train": X[~is_test],
        "y_train": y[~is_test],
        "X_test": X[is_test],
        "y_test": y[is_test],
        "true_w": true_w,
        "W_init": W_init,
    }
