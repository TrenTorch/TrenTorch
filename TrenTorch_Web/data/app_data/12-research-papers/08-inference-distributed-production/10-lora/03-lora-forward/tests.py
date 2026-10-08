"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/10-lora/03-lora-forward/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-lora-forward")
lora_forward = _module.lora_forward


import numpy as np


def test_1_zero_up_projection_matches_the_frozen_layer():
    rng = np.random.default_rng(0)
    x = rng.normal(size=(2, 3))
    W = rng.normal(size=(4, 3))
    out = lora_forward(x, W, rng.normal(size=(2, 3)), np.zeros((4, 2)), 1.0)
    np.testing.assert_allclose(out, x @ W.T)


def test_2_hand_value_on_the_low_rank_path():
    x = np.array([[1.0, 0.0]])
    W = np.zeros((2, 2))
    A = np.array([[1.0, 0.0]])
    B = np.array([[2.0], [0.0]])
    np.testing.assert_allclose(lora_forward(x, W, A, B, 1.0), [[2.0, 0.0]])


def test_3_scale_multiplies_the_adapter_path():
    x = np.array([[1.0, 0.0]])
    W = np.zeros((1, 2))
    A = np.array([[1.0, 0.0]])
    B = np.array([[3.0]])
    np.testing.assert_allclose(lora_forward(x, W, A, B, 0.5), [[1.5]])


def test_4_output_shape():
    assert lora_forward(np.ones((5, 3)), np.ones((4, 3)), np.ones((2, 3)), np.ones((4, 2)), 1.0).shape == (5, 4)


def test_5_equals_merged_weight_forward():
    rng = np.random.default_rng(1)
    x = rng.normal(size=(3, 4))
    W = rng.normal(size=(5, 4))
    A = rng.normal(size=(2, 4))
    B = rng.normal(size=(5, 2))
    merged = W + 0.5 * (B @ A)
    np.testing.assert_allclose(lora_forward(x, W, A, B, 0.5), x @ merged.T)


def test_6_does_not_mutate_inputs():
    x = np.ones((1, 2))
    lora_forward(x, np.ones((1, 2)), np.ones((1, 2)), np.ones((1, 1)), 1.0)
    np.testing.assert_array_equal(x, np.ones((1, 2)))

