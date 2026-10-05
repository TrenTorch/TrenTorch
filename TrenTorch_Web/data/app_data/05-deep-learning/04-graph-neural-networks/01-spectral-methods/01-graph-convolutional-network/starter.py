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
    pass
