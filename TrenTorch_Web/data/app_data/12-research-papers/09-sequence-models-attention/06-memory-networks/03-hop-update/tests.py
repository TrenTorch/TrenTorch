"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/06-memory-networks/03-hop-update/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-memnet-hop")
hop_update = _module.hop_update


import numpy as np


def test_1_adds_the_read_to_the_state():
    np.testing.assert_allclose(hop_update(np.array([1.0, 2.0]), np.array([3.0, 4.0])), [4.0, 6.0])


def test_2_zero_read_leaves_state_unchanged():
    u = np.array([5.0])
    np.testing.assert_allclose(hop_update(u, np.zeros(1)), u)


def test_3_keeps_the_shape():
    assert hop_update(np.ones(4), np.ones(4)).shape == (4,)


def test_4_negative_read_subtracts():
    np.testing.assert_allclose(hop_update(np.array([2.0]), np.array([-1.0])), [1.0])


def test_5_two_hops_accumulate():
    u = hop_update(np.zeros(1), np.array([1.0]))
    u = hop_update(u, np.array([2.0]))
    np.testing.assert_allclose(u, [3.0])


def test_6_does_not_mutate_state():
    u = np.array([1.0])
    hop_update(u, np.array([1.0]))
    np.testing.assert_array_equal(u, [1.0])

