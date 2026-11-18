import numpy as np


def polynomial_features(state, degree):
    """
    Generate polynomial feature expansion.

    Args:
        state: scalar or 1D array state
        degree: polynomial degree

    Returns:
        features: [1, s, s^2, ..., s^degree] normalized
    """
    state = float(state)

    features = np.array([state ** d for d in range(degree + 1)], dtype=np.float32)

    # Normalize: (f - mean) / std
    mean = np.mean(features)
    std = np.std(features)
    if std > 0:
        features = (features - mean) / std

    return features
