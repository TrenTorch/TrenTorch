import numpy as np


def weisfeiler_lehman(adj, num_iterations=3):
    """Perform Weisfeiler-Lehman test iterations.

    Args:
        adj: Adjacency matrix, shape (num_nodes, num_nodes).
        num_iterations: Number of refinement iterations.

    Returns:
        Node color labels, shape (num_nodes,).
    """
    num_nodes = adj.shape[0]
    labels = np.arange(num_nodes, dtype=int)

    for _ in range(num_iterations):
        neighbor_labels = adj @ labels
        new_labels = np.zeros(num_nodes, dtype=int)
        for i in range(num_nodes):
            unique_sorted = tuple(sorted([labels[i], int(neighbor_labels[i])]))
            new_labels[i] = hash(unique_sorted) % (num_nodes * 10)

        labels = new_labels

    return labels
