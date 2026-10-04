import numpy as np


def gat_attention_weights(features, adj):
    """Compute attention weights for GAT.

    Args:
        features: Node features, shape (num_nodes, feature_dim).
        adj: Adjacency matrix, shape (num_nodes, num_nodes).

    Returns:
        Attention weights, shape (num_nodes, num_nodes).
    """
    scores = features @ features.T
    scores = scores / np.sqrt(features.shape[1])

    scores = scores * adj
    scores = scores - (1 - adj) * 1e9

    attention = np.exp(scores - np.max(scores, axis=1, keepdims=True))
    attention = attention * adj
    attention = attention / (np.sum(attention, axis=1, keepdims=True) + 1e-8)

    return attention
