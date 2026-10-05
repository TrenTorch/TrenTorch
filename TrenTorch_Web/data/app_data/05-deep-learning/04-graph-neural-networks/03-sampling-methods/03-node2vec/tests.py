import numpy as np
from _load import load_solution


_module = load_solution(__file__)
biased_random_walk = _module.biased_random_walk


def test_walk_length():
    adj = np.ones((5, 5))
    walk = biased_random_walk(adj, start_node=0, walk_length=10, p=1.0, q=1.0)
    assert walk.shape == (10,)


def test_start_node():
    adj = np.ones((5, 5))
    walk = biased_random_walk(adj, start_node=2, walk_length=5, p=1.0, q=1.0)
    assert walk[0] == 2


def test_all_nodes_valid():
    adj = np.random.randint(0, 2, (8, 8)).astype(float)
    walk = biased_random_walk(adj, start_node=0, walk_length=15, p=0.5, q=2.0)
    assert np.all(walk >= 0) and np.all(walk < 8)


def test_different_p_values():
    adj = np.ones((5, 5))
    np.random.seed(42)
    walk1 = biased_random_walk(adj, start_node=0, walk_length=10, p=0.5, q=1.0)
    np.random.seed(42)
    walk2 = biased_random_walk(adj, start_node=0, walk_length=10, p=2.0, q=1.0)
    assert walk1.shape == walk2.shape


def test_different_q_values():
    adj = np.ones((5, 5))
    np.random.seed(42)
    walk1 = biased_random_walk(adj, start_node=0, walk_length=10, p=1.0, q=0.5)
    np.random.seed(42)
    walk2 = biased_random_walk(adj, start_node=0, walk_length=10, p=1.0, q=2.0)
    assert walk1.shape == walk2.shape


def test_unbiased_uniform_p_q():
    adj = np.ones((4, 4))
    walk = biased_random_walk(adj, start_node=0, walk_length=8, p=1.0, q=1.0)
    assert walk.shape == (8,)


def test_walk_connectivity():
    adj = np.array([[0, 1, 0],
                     [1, 0, 1],
                     [0, 1, 0]], dtype=float)
    walk = biased_random_walk(adj, start_node=0, walk_length=10, p=1.0, q=1.0)
    for i in range(len(walk) - 1):
        assert adj[walk[i], walk[i + 1]] > 0


def test_isolated_node():
    adj = np.zeros((5, 5))
    adj[0, 1] = 1
    adj[1, 0] = 1
    walk = biased_random_walk(adj, start_node=2, walk_length=5, p=1.0, q=1.0)
    assert np.all(walk == 2)


def test_multiple_walks_same_seed():
    adj = np.random.randint(0, 2, (6, 6)).astype(float)
    np.random.seed(0)
    walk1 = biased_random_walk(adj, start_node=0, walk_length=10, p=1.0, q=1.0)
    np.random.seed(0)
    walk2 = biased_random_walk(adj, start_node=0, walk_length=10, p=1.0, q=1.0)
    assert np.array_equal(walk1, walk2)


def test_dtype():
    adj = np.ones((5, 5))
    walk = biased_random_walk(adj, start_node=0, walk_length=10, p=0.5, q=2.0)
    assert walk.dtype in [np.int32, np.int64, int]
