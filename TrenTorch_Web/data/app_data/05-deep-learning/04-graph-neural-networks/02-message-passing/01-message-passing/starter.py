import numpy as np


def message_passing(features, adj, message_fn):
    """Perform message passing on a graph.

    Args:
        features: Node features, shape (num_nodes, feature_dim).
        adj: Adjacency matrix, shape (num_nodes, num_nodes).
        message_fn: Callable taking (sender_features, receiver_features).

    Returns:
        Updated features, shape (num_nodes, feature_dim).
    """
    pass
