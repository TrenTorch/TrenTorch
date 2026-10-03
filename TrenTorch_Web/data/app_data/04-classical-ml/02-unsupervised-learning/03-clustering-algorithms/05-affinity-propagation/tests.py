"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

affinity_propagation = load_solution(__file__).affinity_propagation


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def _two_blobs():
    a = np.array([[0.0, 0.0], [0.1, 0.0], [0.0, 0.1]])
    b = np.array([[10.0, 10.0], [10.1, 10.0], [10.0, 10.1]])
    return np.vstack([a, b])


def test_two_blobs_with_fixed_preference_give_two_clusters():
    labels = affinity_propagation(_two_blobs(), preference=-1.0)
    assert len(np.unique(labels)) == 2


def test_each_blob_gets_one_label():
    labels = affinity_propagation(_two_blobs(), preference=-1.0)
    assert len(set(labels[:3])) == 1
    assert len(set(labels[3:])) == 1
    assert labels[0] != labels[3]


def test_labels_are_consecutive_from_zero():
    labels = affinity_propagation(_two_blobs(), preference=-1.0)
    assert sorted(np.unique(labels).tolist()) == [0, 1]


def test_huge_preference_makes_every_point_an_exemplar():
    X = _two_blobs()
    labels = affinity_propagation(X, preference=0.0)
    assert len(np.unique(labels)) == len(X)


def test_very_negative_preference_gives_one_cluster():
    labels = affinity_propagation(_two_blobs(), preference=-1e6)
    assert np.all(labels == labels[0])


def test_three_blobs_give_three_clusters():
    X = np.vstack([_two_blobs(), [[50.0, 0.0], [50.1, 0.0], [50.0, 0.1]]])
    labels = affinity_propagation(X, preference=-1.0)
    assert len(np.unique(labels)) == 3


def test_output_has_one_label_per_row_and_is_integer():
    X = _two_blobs()
    labels = affinity_propagation(X, preference=-1.0)
    assert labels.shape == (len(X),)
    assert np.issubdtype(labels.dtype, np.integer)


def test_single_point_gets_label_zero():
    assert affinity_propagation(np.array([[2.0, 3.0]])).tolist() == [0]


def test_damping_below_half_raises():
    assert _raises_value_error(affinity_propagation, _two_blobs(), damping=0.3)


def test_damping_one_or_more_raises():
    assert _raises_value_error(affinity_propagation, _two_blobs(), damping=1.0)


def test_translation_does_not_change_the_partition():
    X = _two_blobs()
    a = affinity_propagation(X, preference=-1.0)
    b = affinity_propagation(X + 5.0, preference=-1.0)
    assert np.array_equal(a, b)


def test_scaling_data_and_preference_together_keeps_the_partition():
    X = _two_blobs()
    a = affinity_propagation(X, preference=-1.0)
    b = affinity_propagation(2.0 * X, preference=-4.0)
    assert np.array_equal(a, b)


def test_same_input_gives_same_labels():
    X = _two_blobs()
    assert np.array_equal(affinity_propagation(X, preference=-1.0),
                          affinity_propagation(X, preference=-1.0))


def test_does_not_modify_the_data():
    X = _two_blobs()
    before = X.copy()
    affinity_propagation(X, preference=-1.0)
    assert np.array_equal(X, before)
