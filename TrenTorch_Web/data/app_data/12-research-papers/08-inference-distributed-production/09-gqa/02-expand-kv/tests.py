"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/09-gqa/02-expand-kv/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-gqa-expand-kv")
expand_kv = _module.expand_kv


import numpy as np


def test_1_output_has_one_entry_per_query_head():
    assert expand_kv(np.zeros((2, 3, 4)), 8).shape == (8, 3, 4)


def test_2_repeats_each_group_consecutively():
    kv = np.array([[[1.0]], [[2.0]]])
    out = expand_kv(kv, 4)
    np.testing.assert_allclose(out[:, 0, 0], [1.0, 1.0, 2.0, 2.0])


def test_3_single_kv_head_is_broadcast_to_all():
    out = expand_kv(np.ones((1, 2, 2)), 5)
    np.testing.assert_allclose(out, np.ones((5, 2, 2)))


def test_4_equal_counts_leave_values_unchanged():
    kv = np.arange(4.0).reshape(2, 1, 2)
    np.testing.assert_allclose(expand_kv(kv, 2), kv)


def test_5_values_are_copied_not_shared_for_reading():
    kv = np.ones((1, 1, 1))
    out = expand_kv(kv, 2)
    assert out.shape == (2, 1, 1)


def test_6_does_not_mutate_input():
    kv = np.ones((2, 1, 1))
    expand_kv(kv, 4)
    np.testing.assert_array_equal(kv, np.ones((2, 1, 1)))

