import numpy as np


def laplacian_positional_encoding(adj, k=10):
    """Compute Laplacian positional encoding for nodes.

    Args:
        adj: Adjacency matrix, shape (num_nodes, num_nodes).
        k: Number of eigenvectors to keep.

    Returns:
        Positional encodings, shape (num_nodes, k).
    """
    num_nodes = adj.shape[0]
    degree = np.sum(adj, axis=1)
    d_inv_sqrt = np.diag(1.0 / np.sqrt(degree + 1e-8))

    adj_norm = d_inv_sqrt @ adj @ d_inv_sqrt
    laplacian = np.eye(num_nodes) - adj_norm

    eigenvalues, eigenvectors = np.linalg.eigh(laplacian)
    idx = np.argsort(eigenvalues)
    eigenvectors_sorted = eigenvectors[:, idx]

    k_actual = min(k, num_nodes)
    pe = eigenvectors_sorted[:, :k_actual]

    if k_actual < k:
        pad_width = ((0, 0), (0, k - k_actual))
        pe = np.pad(pe, pad_width, mode='constant', constant_values=0)

    return pe.astype(np.float32)
