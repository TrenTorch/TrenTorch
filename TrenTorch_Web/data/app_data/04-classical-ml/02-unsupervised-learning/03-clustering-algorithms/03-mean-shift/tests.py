"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

mean_shift = load_solution(__file__).mean_shift


def _raises_value_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


def _two_blobs():
    rng = np.random.default_rng(0)
    a = rng.normal(0.0, 0.1, size=(15, 2))
    b = rng.normal(20.0, 0.1, size=(15, 2))
    return np.vstack([a, b])


def test_two_far_blobs_give_two_clusters():
    labels = mean_shift(_two_blobs(), bandwidth=2.0)
    assert len(np.unique(labels)) == 2


def test_each_blob_gets_one_uniform_label():
    labels = mean_shift(_two_blobs(), bandwidth=2.0)
    assert len(set(labels[:15])) == 1
    assert len(set(labels[15:])) == 1
    assert labels[0] != labels[15]


def test_huge_bandwidth_merges_everything_into_one_cluster():
    labels = mean_shift(_two_blobs(), bandwidth=1000.0)
    assert np.all(labels == labels[0])


def test_labels_are_consecutive_from_zero():
    labels = mean_shift(_two_blobs(), bandwidth=2.0)
    assert sorted(np.unique(labels).tolist()) == list(range(len(np.unique(labels))))


def test_output_has_one_label_per_row_and_is_integer():
    X = _two_blobs()
    labels = mean_shift(X, bandwidth=2.0)
    assert labels.shape == (len(X),)
    assert np.issubdtype(labels.dtype, np.integer)


def test_isolated_point_forms_its_own_cluster():
    X = np.vstack([_two_blobs(), [[100.0, 100.0]]])
    labels = mean_shift(X, bandwidth=2.0)
    assert np.sum(labels == labels[-1]) == 1


def test_bandwidth_must_be_positive():
    assert _raises_value_error(mean_shift, _two_blobs(), 0.0)
    assert _raises_value_error(mean_shift, _two_blobs(), -1.0)


def test_single_point_gets_label_zero():
    assert mean_shift(np.array([[3.0, 4.0]]), bandwidth=1.0).tolist() == [0]


def test_tiny_bandwidth_keeps_separated_points_apart():
    X = np.array([[0.0, 0.0], [5.0, 0.0], [10.0, 0.0]])
    labels = mean_shift(X, bandwidth=0.5)
    assert len(np.unique(labels)) == 3


def test_same_input_gives_same_labels():
    X = _two_blobs()
    assert np.array_equal(mean_shift(X, 2.0), mean_shift(X, 2.0))


def test_does_not_modify_the_data():
    X = _two_blobs()
    before = X.copy()
    mean_shift(X, bandwidth=2.0)
    assert np.array_equal(X, before)


def test_label_count_never_exceeds_point_count():
    rng = np.random.default_rng(1)
    X = rng.normal(size=(30, 2))
    labels = mean_shift(X, bandwidth=0.8)
    assert len(np.unique(labels)) <= len(X)


def test_points_in_one_dense_group_share_a_label():
    rng = np.random.default_rng(2)
    X = rng.normal(0.0, 0.05, size=(20, 2))
    labels = mean_shift(X, bandwidth=1.0)
    assert len(np.unique(labels)) == 1
