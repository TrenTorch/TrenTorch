"""
pytest data/app_data/01-numpy/05-broadcasting/06-assemble-normalize-a-batch/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/05-broadcasting/{Path(__file__).resolve().parent.name}")
process_feature_batch = _module.process_feature_batch


def test_scaled_correctness():
    data = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    feature_scales = np.array([10.0, 1.0, 100.0])
    bias_per_sample = np.array([0.0, 0.0])
    result = process_feature_batch(data, feature_scales, bias_per_sample)
    np.testing.assert_array_equal(result["scaled"], [[10, 2, 300], [40, 5, 600]])


def test_biased_correctness_with_correct_reshape_direction():
    data = np.ones((3, 2))
    feature_scales = np.array([1.0, 1.0])
    bias_per_sample = np.array([10.0, 20.0, 30.0])
    result = process_feature_batch(data, feature_scales, bias_per_sample)
    np.testing.assert_array_equal(result["biased"], [[11, 11], [21, 21], [31, 31]])


def test_direct_add_attempt_reports_failure_when_feature_scales_mismatched():
    data = np.ones((3, 4))
    feature_scales_wrong_length = np.array([1.0, 2.0, 3.0])
    bias_per_sample = np.array([1.0, 2.0, 3.0])
    scaled_by_hand = data
    biased_by_hand = scaled_by_hand + bias_per_sample[:, np.newaxis]
    try:
        biased_by_hand + feature_scales_wrong_length
        assert False, "expected ValueError for mismatched feature_scales length"
    except ValueError:
        pass


def test_direct_add_attempt_reports_success_when_shapes_align():
    data = np.ones((3, 4))
    feature_scales = np.array([1.0, 2.0, 3.0, 4.0])
    bias_per_sample = np.array([1.0, 2.0, 3.0])
    result = process_feature_batch(data, feature_scales, bias_per_sample)
    assert result["direct_add_success"] is True
    np.testing.assert_array_equal(
        result["direct_add_result"], result["biased"] + feature_scales
    )


def test_predicted_broadcast_shape_matches_actual_computed_result_shape():
    data = np.ones((3, 4))
    feature_scales = np.array([1.0, 2.0, 3.0, 4.0])
    bias_per_sample = np.array([1.0, 2.0, 3.0])
    result = process_feature_batch(data, feature_scales, bias_per_sample)
    assert result["predicted_broadcast_shape"] == result["biased"].shape
