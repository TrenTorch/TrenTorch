import numpy as np


def make_regression_dataset(
    seed: int,
    n_samples: int,
    n_features: int,
    noise_std: float,
    test_fraction: float,
    hidden_units: int,
) -> dict:
    """
    Create ONE Generator from `seed` and draw from it in EXACTLY this
    order (draw order matters for reproducibility):

      1. X       = rng.standard_normal((n_samples, n_features))
      2. true_w  = rng.uniform(-1.0, 1.0, n_features)
      3. noise   = rng.normal(0.0, noise_std, n_samples)
      4. split   = rng.random(n_samples)
      5. W_init  = he_init-style weights of shape (n_features, hidden_units):
                   rng.normal(0.0, np.sqrt(2.0 / n_features),
                              (n_features, hidden_units))

    Then compute y = X @ true_w + noise.

    Build a boolean mask  is_test = split < test_fraction.
    Rows where is_test is True form the test set; all other rows form
    the train set. Row order within each set must be preserved.

    Return a dictionary with keys:
      "X_train", "y_train", "X_test", "y_test", "true_w", "W_init"

    Shapes: X_train is (n_train, n_features), y_train is (n_train,),
    and so on, where n_train + n_test == n_samples.
    """
    pass
