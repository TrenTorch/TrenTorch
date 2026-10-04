import numpy as np
from _load import load_solution


_module = load_solution(__file__)
weisfeiler_lehman = _module.weisfeiler_lehman


def test_basic_shape():
    adj = np.eye(5)
    labels = weisfeiler_lehman(adj)
    assert labels.shape == (5,)


def test_identity_graph():
    adj = np.eye(5)
    labels = weisfeiler_lehman(adj, num_iterations=1)
    assert labels.shape == (5,)


def test_cycle_graph():
    adj = np.array([[0, 1, 0, 1],
                     [1, 0, 1, 0],
                     [0, 1, 0, 1],
                     [1, 0, 1, 0]], dtype=float)
    labels = weisfeiler_lehman(adj, num_iterations=2)
    assert labels.shape == (4,)


def test_complete_graph():
    n = 5
    adj = np.ones((n, n)) - np.eye(n)
    labels = weisfeiler_lehman(adj)
    assert labels.shape == (n,)


def test_different_iterations():
    adj = np.random.randint(0, 2, (6, 6)).astype(float)
    for num_iter in [1, 2, 3, 5]:
        labels = weisfeiler_lehman(adj, num_iterations=num_iter)
        assert labels.shape == (6,)


def test_finite_labels():
    adj = np.random.randint(0, 2, (10, 10)).astype(float)
    labels = weisfeiler_lehman(adj, num_iterations=3)
    assert np.all(np.isfinite(labels))


def test_labels_are_integers():
    adj = np.random.randint(0, 2, (8, 8)).astype(float)
    labels = weisfeiler_lehman(adj)
    assert labels.dtype in [np.int32, np.int64, int]


def test_sparse_graph():
    adj = np.eye(6)
    adj[0, 1] = 1
    adj[1, 0] = 1
    labels = weisfeiler_lahman(adj, num_iterations=2)
    assert labels.shape == (6,)


def test_star_graph():
    n = 7
    adj = np.zeros((n, n))
    adj[0, 1:] = 1
    adj[1:, 0] = 1
    labels = weisfeiler_lehman(adj, num_iterations=2)
    assert labels.shape == (n,)


def test_convergence():
    adj = np.random.randint(0, 2, (5, 5)).astype(float)
    labels1 = weisfeiler_lehman(adj, num_iterations=5)
    labels2 = weisfeiler_lehman(adj, num_iterations=10)
    assert labels1.shape == labels2.shape
