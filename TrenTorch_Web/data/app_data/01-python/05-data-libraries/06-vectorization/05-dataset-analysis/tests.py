"""
pytest tests.py
"""

import numpy as np
from _load import load_solution

_module = load_solution(__file__)
analyze_dataset = _module.analyze_dataset


def _sample_data():
    return np.array(
        [
            [-4.0, 9.0, 1.0],
            [16.0, -1.0, 25.0],
            [0.0, 4.0, -9.0],
        ]
    )


def test_transformed_correctness():
    data = _sample_data()
    result = analyze_dataset(data, 0, 100)
    np.testing.assert_allclose(result["transformed"], np.sqrt(np.abs(data)))


def test_valid_mask_correctness_with_strict_bounds():
    data = _sample_data()
    result = analyze_dataset(data, 1.0, 4.0)
    transformed = result["transformed"]
    expected = (transformed > 1.0) & (transformed < 4.0)
    np.testing.assert_array_equal(result["valid_mask"], expected)
    assert not np.any(result["valid_mask"] & (transformed == 1.0))
    assert not np.any(result["valid_mask"] & (transformed == 4.0))


def test_valid_count_matches_actual_number_of_true_values():
    data = _sample_data()
    result = analyze_dataset(data, 1.0, 4.0)
    assert result["valid_count"] == int(np.sum(result["valid_mask"]))


def test_feature_means_correct_shape_and_values():
    data = _sample_data()
    result = analyze_dataset(data, 0, 100)
    assert result["feature_means"].shape == (3,)
    np.testing.assert_allclose(result["feature_means"], result["transformed"].mean(axis=0))


def test_sample_maxes_correct_shape_and_values():
    data = _sample_data()
    result = analyze_dataset(data, 0, 100)
    assert result["sample_maxes"].shape == (3,)
    np.testing.assert_allclose(result["sample_maxes"], result["transformed"].max(axis=1))
