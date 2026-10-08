"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/03-gru/03-gru-step/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-gru-step")
gru_step = _module.gru_step


import numpy as np


def test_1_zero_inputs_and_weights_give_zero():
    d = 2
    out = gru_step(np.zeros(d), np.zeros(d), np.zeros((d, d)), np.zeros((d, d)), np.zeros((d, d)), np.zeros((d, d)), np.zeros((d, d)), np.zeros((d, d)))
    np.testing.assert_allclose(out, 0.0)


def test_2_closed_update_gate_keeps_previous_state():
    out = gru_step(np.array([1.0]), np.array([0.3]), np.array([[-100.0]]), np.array([[0.0]]), np.zeros((1, 1)), np.zeros((1, 1)), np.array([[0.5]]), np.zeros((1, 1)))
    np.testing.assert_allclose(out, [0.3], atol=1e-6)


def test_3_open_update_gate_takes_the_candidate():
    out = gru_step(np.array([1.0]), np.array([0.3]), np.array([[100.0]]), np.array([[0.0]]), np.zeros((1, 1)), np.zeros((1, 1)), np.array([[0.5]]), np.zeros((1, 1)))
    np.testing.assert_allclose(out, [np.tanh(0.5)], atol=1e-6)


def test_4_half_gate_averages_old_and_candidate():
    out = gru_step(np.array([0.0]), np.array([1.0]), np.zeros((1, 1)), np.zeros((1, 1)), np.zeros((1, 1)), np.zeros((1, 1)), np.zeros((1, 1)), np.zeros((1, 1)))
    np.testing.assert_allclose(out, [0.5])


def test_5_output_has_hidden_size():
    d_x, d_h = 3, 4
    rng = np.random.default_rng(0)
    out = gru_step(rng.normal(size=d_x), rng.normal(size=d_h), rng.normal(size=(d_h, d_x)), rng.normal(size=(d_h, d_h)), rng.normal(size=(d_h, d_x)), rng.normal(size=(d_h, d_h)), rng.normal(size=(d_h, d_x)), rng.normal(size=(d_h, d_h)))
    assert out.shape == (d_h,)


def test_6_does_not_mutate_the_previous_state():
    h = np.array([0.7])
    gru_step(np.array([1.0]), h, np.ones((1, 1)), np.ones((1, 1)), np.ones((1, 1)), np.ones((1, 1)), np.ones((1, 1)), np.ones((1, 1)))
    np.testing.assert_array_equal(h, [0.7])

