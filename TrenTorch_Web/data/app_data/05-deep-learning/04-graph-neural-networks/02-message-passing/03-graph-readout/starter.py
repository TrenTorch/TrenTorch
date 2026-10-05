import numpy as np


def graph_readout(node_features, readout_type='sum'):
    """Aggregate node features to graph-level representation.

    Args:
        node_features: Node features, shape (num_nodes, feature_dim).
        readout_type: Type of aggregation ('sum', 'mean', 'max').

    Returns:
        Graph-level features, shape (feature_dim,).
    """
    pass
