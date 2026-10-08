"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/03-megatron-lm/01-column-shard/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-megatron-column-shard")
column_shard = _module.column_shard


import numpy as np


def test_1_returns_one_shard_per_device():
    assert len(column_shard(np.zeros((2, 4)), 2)) == 2


def test_2_each_shard_has_a_slice_of_the_columns():
    shards = column_shard(np.zeros((2, 4)), 4)
    assert all(s.shape == (2, 1) for s in shards)


def test_3_concatenating_shards_recovers_the_matrix():
    W = np.arange(8.0).reshape(2, 4)
    np.testing.assert_allclose(np.concatenate(column_shard(W, 2), axis=1), W)


def test_4_single_device_keeps_everything():
    W = np.ones((3, 2))
    np.testing.assert_allclose(column_shard(W, 1)[0], W)


def test_5_shards_hold_consecutive_columns():
    W = np.arange(6.0).reshape(1, 6)
    shards = column_shard(W, 3)
    np.testing.assert_allclose(shards[1], [[2.0, 3.0]])


def test_6_does_not_mutate_weights():
    W = np.ones((2, 2))
    column_shard(W, 2)
    np.testing.assert_array_equal(W, np.ones((2, 2)))

