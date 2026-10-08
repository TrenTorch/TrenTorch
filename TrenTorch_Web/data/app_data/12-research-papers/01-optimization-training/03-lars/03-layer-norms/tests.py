"""
pytest data/app_data/12-research-papers/01-optimization-and-training/03-lars/03-layer-norms/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-lars-layer-norms")
layer_norms = _module.layer_norms


import numpy as np


def test_1_hand_norms():
    assert layer_norms([np.array([3.0, 4.0]), np.array([0.0, 1.0])]) == [5.0, 1.0]


def test_2_one_norm_per_layer():
    assert len(layer_norms([np.ones(2), np.ones(3), np.ones(4)])) == 3


def test_3_each_layer_is_separate():
    a, b = layer_norms([np.array([1.0]), np.array([10.0])])
    assert a == 1.0 and b == 10.0


def test_4_empty_list_gives_empty_list():
    assert layer_norms([]) == []


def test_5_returns_python_floats():
    assert all(isinstance(x, float) for x in layer_norms([np.ones(2)]))


def test_6_matrix_norm_is_frobenius():
    assert abs(layer_norms([np.ones((2, 2))])[0] - 2.0) < 1e-12

