import numpy as np


def sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-z))


def build_features(x: np.ndarray, weight: np.ndarray, bias: np.ndarray) -> np.ndarray:
    """
    Same random-feature construction as `[01-universal-approximation]`'s
    random_hidden_features, but taking an already-drawn weight/bias
    directly (rather than drawing them itself), so the SAME features can
    be built for both a training set and a held-out test set.
    """
    pass


def fit_min_norm(hidden: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Solves for output weights using the Moore-Penrose PSEUDOINVERSE
    (np.linalg.pinv), rather than np.linalg.lstsq. When `hidden` has MORE
    columns (features) than rows (samples), i.e. the overparameterized
    regime, this specific solution is the MINIMUM-NORM one among the
    infinitely many that fit the training data exactly, which is what
    makes this whole demonstration well-defined once num_features exceeds
    the number of training samples.
    """
    pass


def train_and_test_mse(
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_test: np.ndarray,
    y_test: np.ndarray,
    num_features: int,
    rng: np.random.RandomState,
) -> tuple[float, float]:
    """
    Draws `num_features` random hidden units (ONE shared weight/bias
    draw, reused for both the training and test features, so they're
    measured in the same feature space), fits output weights via
    fit_min_norm on the TRAINING set only, and returns
    (train_mse, test_mse).
    """
    pass
