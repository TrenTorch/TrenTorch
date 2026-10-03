import numpy as np


def gaussian_affinities(input: np.ndarray, sigma: float) -> np.ndarray:
    """
    input: shape (n_samples, n_features)
    sigma: the Gaussian kernel's bandwidth (fixed here; real t-SNE picks
    a different sigma per point via a perplexity search, see Theory).

    Returns:
        shape (n_samples, n_samples): p[i, j] is how "similar" point j
        is to point i in the original high-dimensional space, a proper
        probability distribution over j for each fixed i (each row
        sums to 1, and p[i, i] = 0, a point is never its own neighbor).
    """
    # TODO: pairwise_distances(input, input) for the full distance
    # matrix. unnormalized[i,j] = exp(-distance[i,j]^2 / (2*sigma^2)).
    # Zero the diagonal (np.fill_diagonal). Normalize each row to sum
    # to 1.
    pass
