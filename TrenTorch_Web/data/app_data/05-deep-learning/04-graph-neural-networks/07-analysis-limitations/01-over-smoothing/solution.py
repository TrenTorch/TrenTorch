import numpy as np


def detect_over_smoothing(features, adj, num_layers):
    """Detect over-smoothing by measuring feature divergence.

    Args:
        features: Node features, shape (num_nodes, feature_dim).
        adj: Adjacency matrix, shape (num_nodes, num_nodes).
        num_layers: Number of GNN layers to simulate.

    Returns:
        Divergence scores per layer, shape (num_layers,).
    """
    num_nodes = adj.shape[0]
    degree = np.sum(adj, axis=1)
    degree_inv = 1.0 / (degree + 1e-8)
    d_inv = np.diag(degree_inv)

    adj_norm = d_inv @ adj

    divergence_scores = []
    current = features.copy()

    for _ in range(num_layers):
        current = adj_norm @ current

        feature_var = np.var(current, axis=0)
        divergence = np.mean(feature_var)
        divergence_scores.append(divergence)

    return np.array(divergence_scores, dtype=np.float32)
