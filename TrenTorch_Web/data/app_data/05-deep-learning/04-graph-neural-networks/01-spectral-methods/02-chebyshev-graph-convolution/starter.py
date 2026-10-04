import numpy as np


def chebyshev_conv(features, adj, weight, k=3):
    """Apply Chebyshev graph convolution.

    Args:
        features: Node features, shape (num_nodes, input_dim).
        adj: Adjacency matrix, shape (num_nodes, num_nodes).
        weight: Weight matrix, shape (k+1, input_dim, output_dim).
        k: Order of Chebyshev polynomial.

    Returns:
        Updated features, shape (num_nodes, output_dim).
    """
    pass
