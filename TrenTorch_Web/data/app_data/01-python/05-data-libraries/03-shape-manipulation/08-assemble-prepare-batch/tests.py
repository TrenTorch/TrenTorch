"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
prepare_batch = _module.prepare_batch


def test_batch_correct_shape_and_value_order():
    flat_data = np.arange(12)
    result = prepare_batch(flat_data, batch_size=3, feature_count=4, num_groups=2)
    assert result["batch"].shape == (3, 4)
    np.testing.assert_array_equal(result["batch"][0], [0, 1, 2, 3])
    np.testing.assert_array_equal(result["batch"][1], [4, 5, 6, 7])


def test_transposed_correct_shape_and_values():
    flat_data = np.arange(12)
    result = prepare_batch(flat_data, batch_size=3, feature_count=4, num_groups=2)
    assert result["transposed"].shape == (4, 3)
    np.testing.assert_array_equal(result["transposed"], result["batch"].T)


def test_with_channel_correct_shape():
    flat_data = np.arange(12)
    result = prepare_batch(flat_data, batch_size=3, feature_count=4, num_groups=2)
    assert result["with_channel"].shape == (1, 4, 3)


def test_groups_correct_count_shapes_and_values():
    flat_data = np.arange(12)
    result = prepare_batch(flat_data, batch_size=3, feature_count=4, num_groups=2)
    groups = result["groups"]
    assert len(groups) == 2
    for group in groups:
        assert group.shape == (1, 2, 3)
    reconstructed = np.concatenate(groups, axis=1)
    np.testing.assert_array_equal(reconstructed, result["with_channel"])


def test_memory_sharing_correctness_through_full_chain():
    flat_data = np.arange(12)
    result = prepare_batch(flat_data, batch_size=3, feature_count=4, num_groups=2)
    assert result["with_channel_shares_memory_with_flat_data"] is True
    assert result["groups_first_shares_memory_with_flat_data"] is True


def test_mutation_at_start_propagates_to_end_of_chain():
    flat_data = np.arange(12)
    result = prepare_batch(flat_data, batch_size=3, feature_count=4, num_groups=2)
    flat_data[0] = -1
    assert result["groups"][0][0, 0, 0] == -1
