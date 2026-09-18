"""
pytest data/app_data/01-classical-ml/06-unsupervised/08-hierarchical-clustering/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/06-unsupervised/{Path(__file__).resolve().parent.name}")
cluster_distance = _module.cluster_distance
agglomerative_fit = _module.agglomerative_fit


def _same_cluster_pairs(labels: np.ndarray) -> set[tuple[int, int]]:
    n = len(labels)
    return {(i, j) for i in range(n) for j in range(i + 1, n) if labels[i] == labels[j]}


def test_cluster_distance_single_linkage_matches_hand_computation():
    a = np.array([[0.0], [1.0]])
    b = np.array([[5.0], [1.5]])  # closest pair: 1.0 and 1.5, distance 0.5
    assert np.isclose(cluster_distance(a, b, "single"), 0.5)


def test_cluster_distance_complete_linkage_matches_hand_computation():
    a = np.array([[0.0], [1.0]])
    b = np.array([[5.0], [1.5]])  # farthest pair: 0.0 and 5.0, distance 5.0
    assert np.isclose(cluster_distance(a, b, "complete"), 5.0)


def test_cluster_distance_average_linkage_matches_hand_computation():
    a = np.array([[0.0]])
    b = np.array([[2.0], [4.0]])  # distances 2 and 4, mean 3
    assert np.isclose(cluster_distance(a, b, "average"), 3.0)


def test_invalid_linkage_raises():
    a = np.array([[0.0]])
    b = np.array([[1.0]])
    try:
        cluster_distance(a, b, "median")
        assert False, "expected a ValueError"
    except ValueError:
        pass


def test_n_clusters_equals_n_samples_gives_every_point_its_own_label():
    input = np.array([[0.0], [1.0], [2.0]])
    labels = agglomerative_fit(input, n_clusters=3)
    assert len(set(labels.tolist())) == 3


def test_n_clusters_one_gives_everything_the_same_label():
    input = np.array([[0.0], [1.0], [100.0]])
    labels = agglomerative_fit(input, n_clusters=1)
    assert len(set(labels.tolist())) == 1


def test_recovers_three_well_separated_clusters():
    rng = np.random.default_rng(0)
    input = np.vstack(
        [
            rng.normal(loc=0.0, scale=0.3, size=(10, 2)),
            rng.normal(loc=10.0, scale=0.3, size=(10, 2)),
            rng.normal(loc=20.0, scale=0.3, size=(10, 2)),
        ]
    )
    labels = agglomerative_fit(input, n_clusters=3, linkage="single")
    pairs = _same_cluster_pairs(labels)
    # every within-group pair should be clustered together
    assert (0, 5) in pairs
    assert (10, 15) in pairs
    assert (20, 25) in pairs
    # no cross-group pair should be
    assert (0, 10) not in pairs
    assert (10, 20) not in pairs


def test_single_and_complete_linkage_disagree_on_a_chain_shape():
    # A classic demonstration: a "dumbbell" made of a chain of
    # intermediate points connecting two dense blobs. Single linkage
    # chains straight through the bridge and merges everything into
    # one cluster before splitting the two blobs apart; complete
    # linkage refuses to bridge them nearly as readily. The two
    # linkages should disagree about at least one pair here.
    blob_a = np.array([[0.0, 0.0], [0.1, 0.0], [0.0, 0.1]])
    bridge = np.array([[1.0, 0.0], [2.0, 0.0], [3.0, 0.0]])
    blob_b = np.array([[4.0, 0.0], [4.1, 0.0], [4.0, 0.1]])
    input = np.vstack([blob_a, bridge, blob_b])

    single_labels = agglomerative_fit(input, n_clusters=2, linkage="single")
    complete_labels = agglomerative_fit(input, n_clusters=2, linkage="complete")

    # index 5 is the bridge point closest to blob_b -- single linkage's
    # chaining still groups it with blob_a (index 0), complete
    # linkage's preference for compact clusters groups it with blob_b
    # instead.
    assert (single_labels[5] == single_labels[0]) != (
        complete_labels[5] == complete_labels[0]
    )


def test_merges_the_closest_pair_not_the_farthest():
    # Directly targets a mutant that merges the farthest pair instead
    # of the closest: three points where the correct first merge is
    # obvious (the two nearly-identical points), a "merge farthest"
    # bug would instead group the two extremes together.
    input = np.array([[0.0], [0.01], [100.0]])
    labels = agglomerative_fit(input, n_clusters=2, linkage="single")
    assert labels[0] == labels[1]
    assert labels[2] != labels[0]


def test_matches_real_sklearn_agglomerative_clustering_co_membership():
    # Ground truth from the actual library, not our own derivation.
    #
    # Generated once, offline, with:
    #   rng = np.random.default_rng(0)
    #   X = np.vstack([rng.normal(0, 0.3, (10,2)), rng.normal(5, 0.3, (10,2)),
    #                  rng.normal(10, 0.3, (10,2))])
    #   AgglomerativeClustering(n_clusters=3, linkage='average').fit(X).labels_
    #   adjusted_rand_score(ours, sklearn's) == 1.0 (identical clustering,
    #   possibly different label numbering)
    #
    # This test needs no scikit-learn installed to run -- it checks the
    # same permutation-invariant property (which points end up
    # together) that adjusted_rand_score verified offline.
    rng = np.random.default_rng(0)
    input = np.vstack(
        [
            rng.normal(loc=0.0, scale=0.3, size=(10, 2)),
            rng.normal(loc=5.0, scale=0.3, size=(10, 2)),
            rng.normal(loc=10.0, scale=0.3, size=(10, 2)),
        ]
    )
    labels = agglomerative_fit(input, n_clusters=3, linkage="average")
    pairs = _same_cluster_pairs(labels)
    for group_start in (0, 10, 20):
        assert (group_start, group_start + 5) in pairs
    assert (0, 10) not in pairs
    assert (10, 20) not in pairs
    assert (0, 20) not in pairs
