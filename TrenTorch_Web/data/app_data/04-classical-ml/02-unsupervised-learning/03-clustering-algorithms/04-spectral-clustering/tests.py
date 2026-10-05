"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

spectral_clustering = load_solution(__file__).spectral_clustering


def _raises_value_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


def _block_graph(cross=0.0):
    # two disjoint groups of three nodes, all-ones within each group
    W = np.zeros((6, 6))
    W[:3, :3] = 1.0
    W[3:, 3:] = 1.0
    W[:3, 3:] = cross
    W[3:, :3] = cross
    return W


def test_disjoint_groups_are_recovered():
    labels = spectral_clustering(_block_graph(), 2)
    assert len(set(labels[:3])) == 1
    assert len(set(labels[3:])) == 1
    assert labels[0] != labels[3]


def test_weak_cross_links_do_not_change_the_grouping():
    labels = spectral_clustering(_block_graph(cross=0.01), 2)
    assert len(set(labels[:3])) == 1
    assert len(set(labels[3:])) == 1
    assert labels[0] != labels[3]


def test_k_one_puts_everything_together():
    assert np.all(spectral_clustering(_block_graph(), 1) == 0)


def test_labels_have_one_entry_per_node_within_range():
    labels = spectral_clustering(_block_graph(), 2)
    assert labels.shape == (6,)
    assert set(labels.tolist()).issubset({0, 1})


def test_three_blocks_give_three_clusters():
    W = np.zeros((9, 9))
    for start in (0, 3, 6):
        W[start:start + 3, start:start + 3] = 1.0
    labels = spectral_clustering(W, 3)
    assert len({labels[0], labels[3], labels[6]}) == 3
    for start in (0, 3, 6):
        assert len(set(labels[start:start + 3])) == 1


def test_same_graph_gives_same_labels_every_time():
    W = _block_graph(cross=0.02)
    assert np.array_equal(spectral_clustering(W, 2), spectral_clustering(W, 2))


def test_non_square_matrix_raises():
    assert _raises_value_error(spectral_clustering, np.ones((2, 3)), 2)


def test_asymmetric_matrix_raises():
    W = np.array([[0.0, 1.0], [0.0, 0.0]])
    assert _raises_value_error(spectral_clustering, W, 2)


def test_k_out_of_range_raises():
    assert _raises_value_error(spectral_clustering, _block_graph(), 0)
    assert _raises_value_error(spectral_clustering, _block_graph(), 7)


def test_does_not_modify_the_affinity_matrix():
    W = _block_graph(cross=0.05)
    before = W.copy()
    spectral_clustering(W, 2)
    assert np.array_equal(W, before)


def test_isolated_node_does_not_crash():
    W = _block_graph()
    W[5, :] = 0.0
    W[:, 5] = 0.0
    labels = spectral_clustering(W, 2)
    assert labels.shape == (6,)


def test_label_renaming_of_nodes_moves_the_grouping_with_them():
    W = _block_graph()
    perm = np.array([3, 0, 4, 1, 5, 2])
    labels = spectral_clustering(W[np.ix_(perm, perm)], 2)
    assert len(set(labels[[1, 3, 5]])) == 1
    assert len(set(labels[[0, 2, 4]])) == 1
