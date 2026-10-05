import numpy as np
from _load import load_solution


_module = load_solution(__file__)
random_walk = _module.random_walk


def test_walk_length():
    adj = np.eye(5)
    walk = random_walk(adj, start_node=0, walk_length=10)
    assert walk.shape == (10,)


def test_start_node_in_walk():
    adj = np.eye(5)
    walk = random_walk(adj, start_node=2, walk_length=5)
    assert walk[0] == 2


def test_all_nodes_valid():
    adj = np.random.randint(0, 2, (10, 10)).astype(float)
    for _ in range(5):
        walk = random_walk(adj, start_node=0, walk_length=20)
        assert np.all(walk >= 0) and np.all(walk < 10)


def test_identity_adjacency():
    adj = np.eye(5)
    np.random.seed(42)
    walk = random_walk(adj, start_node=1, walk_length=5)
    assert walk[0] == 1


def test_connected_graph():
    adj = np.ones((4, 4))
    walk = random_walk(adj, start_node=0, walk_length=8)
    assert walk.shape == (8,)


def test_single_node_walk():
    adj = np.eye(3)
    walk = random_walk(adj, start_node=1, walk_length=1)
    assert walk.shape == (1,) and walk[0] == 1


def test_different_walk_lengths():
    adj = np.random.randint(0, 2, (8, 8)).astype(float)
    for length in [1, 5, 10, 20]:
        walk = random_walk(adj, start_node=0, walk_length=length)
        assert walk.shape == (length,)


def test_walk_dtype():
    adj = np.random.randint(0, 2, (6, 6)).astype(float)
    walk = random_walk(adj, start_node=0, walk_length=10)
    assert walk.dtype in [np.int32, np.int64, int]


def test_walk_connectivity():
    adj = np.array([[0, 1, 0],
                     [1, 0, 1],
                     [0, 1, 0]], dtype=float)
    walk = random_walk(adj, start_node=0, walk_length=10)
    for i in range(len(walk) - 1):
        assert adj[walk[i], walk[i + 1]] > 0


def test_isolated_node_walk():
    adj = np.zeros((5, 5))
    adj[0, 1] = 1
    adj[1, 0] = 1
    walk = random_walk(adj, start_node=2, walk_length=5)
    assert walk[0] == 2
    assert np.all(walk == 2)
