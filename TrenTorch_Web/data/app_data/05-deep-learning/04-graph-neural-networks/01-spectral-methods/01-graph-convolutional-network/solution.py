import numpy as np


def gcn_layer(features, adj, weight):
    """Apply one GCN layer.

    Args:
        features: Node features, shape (num_nodes, input_dim).
        adj: Adjacency matrix, shape (num_nodes, num_nodes).
        weight: Weight matrix, shape (input_dim, output_dim).

    Returns:
        Updated features, shape (num_nodes, output_dim).
    """
    degree = np.sum(adj, axis=1)
    degree_inv_sqrt = 1.0 / np.sqrt(degree + 1e-8)
    d_inv_sqrt = np.diag(degree_inv_sqrt)

    normalized_adj = d_inv_sqrt @ adj @ d_inv_sqrt

    aggregated = normalized_adj @ features
    output = aggregated @ weight

    return output
