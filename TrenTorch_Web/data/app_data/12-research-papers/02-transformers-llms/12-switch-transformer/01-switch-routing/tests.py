"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/12-switch-transformer/01-switch-routing/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-switch-routing")
switch_route = _module.switch_route


import numpy as np


def test_1_output_shapes_are_one_per_token():
    idx, gate = switch_route(np.zeros((5, 3)))
    assert idx.shape == (5,) and gate.shape == (5,)


def test_2_strong_preference_selects_that_expert_with_high_gate():
    idx, gate = switch_route(np.array([[0.0, 10.0]]))
    assert idx[0] == 1 and gate[0] > 0.99


def test_3_uniform_logits_pick_the_first_expert():
    idx, _ = switch_route(np.zeros((1, 4)))
    assert idx[0] == 0


def test_4_gate_is_a_probability():
    rng = np.random.default_rng(0)
    _, gate = switch_route(rng.normal(size=(6, 4)))
    assert np.all(gate > 0) and np.all(gate <= 1)


def test_5_matches_a_hand_computed_gate():
    _, gate = switch_route(np.array([[0.0, np.log(3.0)]]))
    assert abs(gate[0] - 0.75) < 1e-12


def test_6_does_not_mutate_inputs():
    logits = np.array([[1.0, 2.0]])
    switch_route(logits)
    np.testing.assert_array_equal(logits, [[1.0, 2.0]])

