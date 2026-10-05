import numpy as np


def biased_random_walk(adj, start_node, walk_length, p, q):
    """Perform a biased random walk (node2vec).

    Args:
        adj: Adjacency matrix, shape (num_nodes, num_nodes).
        start_node: Starting node index.
        walk_length: Length of the walk.
        p: Return parameter.
        q: In-out parameter.

    Returns:
        Node indices in the walk, shape (walk_length,).
    """
    pass
