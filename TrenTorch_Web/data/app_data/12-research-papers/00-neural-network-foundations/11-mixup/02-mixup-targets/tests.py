"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/11-mixup/02-mixup-targets/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-mixup-targets")
mixup_targets = _module.mixup_targets


import numpy as np


def test_1_one_hot_labels_blend_correctly():
    y = np.array([[1.0, 0.0], [0.0, 1.0]])
    np.testing.assert_allclose(mixup_targets(y, np.array([1, 0]), 0.25), [[0.25, 0.75], [0.75, 0.25]])


def test_2_targets_still_sum_to_one_per_example():
    y = np.eye(3)
    out = mixup_targets(y, np.array([2, 0, 1]), 0.4)
    np.testing.assert_allclose(out.sum(axis=1), 1.0)


def test_3_lam_one_keeps_original_labels():
    y = np.eye(2)
    np.testing.assert_allclose(mixup_targets(y, np.array([1, 0]), 1.0), y)


def test_4_identity_permutation_keeps_labels():
    y = np.eye(2)
    np.testing.assert_allclose(mixup_targets(y, np.array([0, 1]), 0.3), y)


def test_5_keeps_the_label_shape():
    assert mixup_targets(np.eye(4), np.array([3, 2, 1, 0]), 0.5).shape == (4, 4)


def test_6_does_not_mutate_the_labels():
    y = np.eye(2)
    mixup_targets(y, np.array([1, 0]), 0.5)
    np.testing.assert_array_equal(y, np.eye(2))

