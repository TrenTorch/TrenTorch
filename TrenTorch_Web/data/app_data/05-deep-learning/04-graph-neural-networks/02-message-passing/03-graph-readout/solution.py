import numpy as np


def graph_readout(node_features, readout_type='sum'):
    """Aggregate node features to graph-level representation.

    Args:
        node_features: Node features, shape (num_nodes, feature_dim).
        readout_type: Type of aggregation ('sum', 'mean', 'max').

    Returns:
        Graph-level features, shape (feature_dim,).
    """
    if readout_type == 'sum':
        return np.sum(node_features, axis=0)
    elif readout_type == 'mean':
        return np.mean(node_features, axis=0)
    elif readout_type == 'max':
        return np.max(node_features, axis=0)
    else:
        raise ValueError(f"Unknown readout_type: {readout_type}")
