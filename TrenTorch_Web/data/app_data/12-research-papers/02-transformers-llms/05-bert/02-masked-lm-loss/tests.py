"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/05-bert/02-masked-lm-loss/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-bert-masked-lm-loss")
masked_lm_loss = _module.masked_lm_loss


import numpy as np


def test_1_uniform_predictions_give_log_v_over_masked_positions():
    lp = np.full((4, 5), np.log(0.2))
    out = masked_lm_loss(lp, np.array([0, 1, 2, 3]), np.array([True, True, True, True]))
    assert abs(out - np.log(5.0)) < 1e-9


def test_2_unmasked_positions_are_ignored():
    lp = np.log(np.full((3, 2), 0.5))
    lp[1] = np.log(np.array([1e-9, 1.0]))
    out = masked_lm_loss(lp, np.array([0, 0, 0]), np.array([True, False, True]))
    assert abs(out - np.log(2.0)) < 1e-9


def test_3_no_masked_positions_gives_zero():
    lp = np.log(np.full((2, 2), 0.5))
    assert masked_lm_loss(lp, np.array([0, 1]), np.array([False, False])) == 0.0


def test_4_perfect_predictions_give_zero():
    lp = np.log(np.eye(3) + 1e-300)
    out = masked_lm_loss(lp, np.array([0, 1, 2]), np.array([True, True, True]))
    assert abs(out) < 1e-9


def test_5_returns_a_python_float():
    lp = np.log(np.full((1, 2), 0.5))
    assert isinstance(masked_lm_loss(lp, np.array([0]), np.array([True])), float)


def test_6_does_not_mutate_inputs():
    lp = np.log(np.full((2, 2), 0.5))
    masked_lm_loss(lp, np.array([0, 1]), np.array([True, True]))
    np.testing.assert_allclose(lp, np.log(np.full((2, 2), 0.5)))

