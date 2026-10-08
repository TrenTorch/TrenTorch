"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/06-gpt-3/02-causal-mask/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-causal-mask")
causal_mask = _module.causal_mask


import numpy as np


def test_1_shape_is_n_by_n():
    assert causal_mask(4).shape == (4, 4)


def test_2_is_lower_triangular():
    m = causal_mask(3)
    np.testing.assert_array_equal(m, [[True, False, False], [True, True, False], [True, True, True]])


def test_3_diagonal_is_always_true():
    assert causal_mask(5).diagonal().all()


def test_4_upper_triangle_is_all_false():
    m = causal_mask(4)
    assert not np.triu(m, k=1).any()


def test_5_counts_allowed_pairs():
    assert causal_mask(5).sum() == 5 * 6 // 2


def test_6_single_position_attends_only_to_itself():
    np.testing.assert_array_equal(causal_mask(1), [[True]])

