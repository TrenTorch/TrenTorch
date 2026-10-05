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
    num_nodes = features.shape[0]
    aggregated = np.zeros_like(features)

    for i in range(num_nodes):
        neighbors = np.where(adj[i] > 0)[0]
        if len(neighbors) > 0:
            sampled = np.random.choice(neighbors, size=min(num_samples, len(neighbors)), replace=False)
            aggregated[i] = np.mean(features[sampled], axis=0)
        else:
            aggregated[i] = features[i]

    output = aggregated @ weight
    return output
