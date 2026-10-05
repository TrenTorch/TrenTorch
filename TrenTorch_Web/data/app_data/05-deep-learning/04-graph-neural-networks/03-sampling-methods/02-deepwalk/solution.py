import numpy as np


def random_walk(adj, start_node, walk_length):
    """Perform a random walk on the graph.

    Args:
        adj: Adjacency matrix, shape (num_nodes, num_nodes).
        start_node: Starting node index.
        walk_length: Length of the walk.

    Returns:
        Node indices in the walk, shape (walk_length,).
    """
    walk = [start_node]
    current = start_node

    for _ in range(walk_length - 1):
        neighbors = np.where(adj[current] > 0)[0]
        if len(neighbors) == 0:
            next_node = current
        else:
            next_node = np.random.choice(neighbors)
        walk.append(next_node)
        current = next_node

    return np.array(walk, dtype=int)
