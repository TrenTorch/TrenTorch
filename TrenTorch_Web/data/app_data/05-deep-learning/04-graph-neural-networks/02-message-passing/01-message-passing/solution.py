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
    num_nodes = features.shape[0]
    messages = np.zeros_like(features)

    for i in range(num_nodes):
        neighbors = np.where(adj[i] > 0)[0]
        for j in neighbors:
            msg = message_fn(features[j], features[i])
            messages[i] = messages[i] + msg

    if np.sum(adj) > 0:
        messages = messages / (np.sum(adj, axis=1, keepdims=True) + 1e-8)

    return messages
