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
    pass
