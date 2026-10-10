import numpy as np


def gin_layer(features, adj, weight, epsilon=0.0):
    """Apply GIN layer.

    Args:
        features: Node features, shape (num_nodes, input_dim).
        adj: Adjacency matrix, shape (num_nodes, num_nodes).
        weight: Weight matrix, shape (input_dim, output_dim).
        epsilon: Scalar parameter.

    Returns:
        Updated features, shape (num_nodes, output_dim).
    """
    neighbors = np.array(adj, dtype=float)
    np.fill_diagonal(neighbors, 0.0)
    neighbor_sum = neighbors @ features
    scaled_center = (1.0 + epsilon) * features
    aggregated = scaled_center + neighbor_sum
    output = aggregated @ weight
    return output
