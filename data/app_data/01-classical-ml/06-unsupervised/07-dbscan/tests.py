"""
pytest data/app_data/01-classical-ml/06-unsupervised/07-dbscan/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/06-unsupervised/{Path(__file__).resolve().parent.name}")
region_query = _module.region_query
dbscan_fit = _module.dbscan_fit


def test_region_query_matches_hand_computation():
    input = np.array([[0.0], [1.0], [2.0], [10.0]])
    result = region_query(input, point_idx=1, eps=1.5)
    assert set(result.tolist()) == {0, 1, 2}


def test_region_query_includes_the_point_itself():
    input = np.array([[5.0]])
    result = region_query(input, point_idx=0, eps=0.0)
    assert list(result) == [0]


def test_two_dense_clusters_and_noise_are_separated_correctly():
    rng = np.random.default_rng(0)
    cluster0 = rng.normal(loc=0.0, scale=0.3, size=(20, 2))
    cluster1 = rng.normal(loc=5.0, scale=0.3, size=(20, 2))
    noise = np.array([[10.0, 10.0], [-10.0, -10.0]])
    input = np.vstack([cluster0, cluster1, noise])

    labels = dbscan_fit(input, eps=0.8, min_samples=5)

    assert len(np.unique(labels[:20])) == 1 and labels[0] != -1
    assert len(np.unique(labels[20:40])) == 1 and labels[20] != -1
    assert labels[0] != labels[20]  # the two clusters are distinct
    assert labels[-1] == -1 and labels[-2] == -1  # both noise points isolated


def test_min_samples_too_high_marks_everything_as_noise():
    rng = np.random.default_rng(1)
    input = rng.normal(size=(15, 2))
    labels = dbscan_fit(input, eps=0.1, min_samples=1000)
    assert np.all(labels == -1)


def test_border_point_joins_cluster_without_extending_it():
    # A tight core cluster of 4 points, plus one point close to the
    # cluster's edge but too isolated to be a core point itself. That
    # edge point must join the cluster (border point), but nothing
    # beyond it should be picked up.
    core_cluster = np.array([[0.0, 0.0], [0.1, 0.0], [0.0, 0.1], [0.1, 0.1]])
    border_point = np.array([[0.5, 0.0]])  # within eps of the cluster, but alone
    far_away = np.array([[5.0, 5.0]])
    input = np.vstack([core_cluster, border_point, far_away])

    labels = dbscan_fit(input, eps=0.5, min_samples=4)

    assert labels[4] == labels[0]  # border point joined the cluster
    assert labels[5] == -1  # far point never reached


def test_expansion_only_continues_through_core_points_not_any_neighbor():
    # Directly targets a mutant that appends EVERY visited neighbor's
    # own neighbors to the growth queue (not just core points' ones):
    # a "chain" of points spaced so that each is within eps of the
    # next, but no single point (besides the seed cluster) has enough
    # neighbors to be core on its own. A correct implementation stops
    # the chain from fully connecting into one giant cluster; an
    # over-expansive one connects everything.
    core = np.array([[0.0, 0.0], [0.05, 0.0], [0.0, 0.05], [0.05, 0.05], [0.02, 0.02]])
    chain = np.array([[0.5 * i, 0.0] for i in range(1, 6)])  # spaced 0.5 apart, isolated
    input = np.vstack([core, chain])

    labels = dbscan_fit(input, eps=0.51, min_samples=5)

    assert not np.all(labels[len(core) :] == labels[0])


def test_matches_real_sklearn_dbscan_on_a_baked_dataset():
    # Ground truth from the actual library, not our own derivation.
    #
    # Generated once, offline, with:
    #   rng = np.random.default_rng(0)
    #   X = np.vstack([rng.normal(0, 0.3, (20,2)), rng.normal(5, 0.3, (20,2)),
    #                  rng.uniform(-5, 10, (5,2))])
    #   DBSCAN(eps=0.8, min_samples=5).fit(X).labels_  # baked below
    #
    # This test needs no scikit-learn installed to run.
    rng = np.random.default_rng(0)
    cluster0 = rng.normal(loc=0, scale=0.3, size=(20, 2))
    cluster1 = rng.normal(loc=5, scale=0.3, size=(20, 2))
    noise = rng.uniform(-5, 10, size=(5, 2))
    input = np.vstack([cluster0, cluster1, noise])

    labels = dbscan_fit(input, eps=0.8, min_samples=5)
    expected = np.array(
        [0] * 20 + [1] * 20 + [-1, -1, -1, -1, -1]
    )
    assert np.array_equal(labels, expected)
