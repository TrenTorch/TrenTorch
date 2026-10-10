import numpy as np


def rbf_features(state, centers, sigma=1.0):
    """
    Compute RBF features.

    Args:
        state: current state (scalar or vector)
        centers: array of center points
        sigma: RBF width parameter

    Returns:
        features: RBF feature vector of shape (num_centers,)
    """
    state = np.atleast_1d(np.array(state, dtype=np.float32))
    centers = np.array(centers, dtype=np.float32)
    if centers.ndim == 1:
        centers = centers.reshape(-1, state.shape[-1])

    # Compute distances from state to each center
    differences = centers - state
    distances = np.linalg.norm(differences, axis=-1)

    # RBF kernel: exp(-distance^2 / (2 * sigma^2))
    features = np.exp(-distances ** 2 / (2 * sigma ** 2))

    return features.astype(np.float32)
