"""
pytest data/01-classical-ml/02-classification/04-decision-boundary/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

predict_labels = load_solution(f"01-classical-ml/02-classification/{Path(__file__).resolve().parent.name}").predict_labels


def test_above_and_below_threshold():
    p = np.array([0.9, 0.1, 0.6, 0.4])
    assert np.array_equal(predict_labels(p), [1, 0, 1, 0])


def test_exactly_at_threshold_predicts_positive():
    assert predict_labels(np.array([0.5]))[0] == 1


def test_custom_threshold():
    p = np.array([0.7, 0.3])
    assert np.array_equal(predict_labels(p, threshold=0.8), [0, 0])
    assert np.array_equal(predict_labels(p, threshold=0.2), [1, 1])


def test_output_dtype_is_integer():
    result = predict_labels(np.array([0.9, 0.1]))
    assert np.issubdtype(result.dtype, np.integer)


def test_all_same_value():
    assert np.array_equal(predict_labels(np.full(5, 0.5)), np.ones(5))
