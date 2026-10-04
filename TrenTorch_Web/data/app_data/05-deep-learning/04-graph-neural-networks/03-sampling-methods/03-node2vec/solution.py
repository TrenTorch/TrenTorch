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
    walk = [start_node]
    prev = None
    current = start_node

    for _ in range(walk_length - 1):
        neighbors = np.where(adj[current] > 0)[0]
        if len(neighbors) == 0:
            next_node = current
        else:
            if prev is None:
                probs = np.ones(len(neighbors)) / len(neighbors)
            else:
                probs = np.zeros(len(neighbors))
                for i, neighbor in enumerate(neighbors):
                    if neighbor == prev:
                        probs[i] = 1.0 / p
                    elif adj[prev, neighbor] > 0:
                        probs[i] = 1.0
                    else:
                        probs[i] = 1.0 / q
                probs = probs / np.sum(probs)

            next_node = np.random.choice(neighbors, p=probs)

        walk.append(next_node)
        prev = current
        current = next_node

    return np.array(walk, dtype=int)
