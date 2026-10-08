"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/04-attention-is-all-you-need/02-split-heads/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-multihead-split")
split_heads = _module.split_heads


import numpy as np


def test_1_output_shape():
    assert split_heads(np.ones((5, 8)), 4).shape == (4, 5, 2)


def test_2_hand_computed_split():
    x = np.array([[1.0, 2.0, 3.0, 4.0]])
    np.testing.assert_allclose(split_heads(x, 2), [[[1.0, 2.0]], [[3.0, 4.0]]])


def test_3_one_head_adds_a_leading_axis():
    x = np.arange(6.0).reshape(3, 2)
    out = split_heads(x, 1)
    assert out.shape == (1, 3, 2)
    np.testing.assert_allclose(out[0], x)


def test_4_splitting_is_reversible():
    rng = np.random.default_rng(0)
    x = rng.normal(size=(4, 6))
    out = split_heads(x, 3)
    merged = out.transpose(1, 0, 2).reshape(4, 6)
    np.testing.assert_allclose(merged, x)


def test_5_each_head_sees_a_disjoint_slice_of_features():
    x = np.arange(8.0).reshape(1, 8)
    out = split_heads(x, 4)
    assert len(np.unique(out)) == 8


def test_6_does_not_mutate_the_input():
    x = np.ones((2, 4))
    split_heads(x, 2)
    np.testing.assert_array_equal(x, np.ones((2, 4)))

