import numpy as np


def graphsage_layer(features, adj, weight, num_samples):
    """Apply GraphSAGE layer with neighbor sampling.

    Args:
        features: Node features, shape (num_nodes, input_dim).
        adj: Adjacency matrix, shape (num_nodes, num_nodes).
        weight: Weight matrix, shape (input_dim, output_dim).
        num_samples: Number of neighbors to sample per node.

    Returns:
        Updated features, shape (num_nodes, output_dim).
    """
    pass
