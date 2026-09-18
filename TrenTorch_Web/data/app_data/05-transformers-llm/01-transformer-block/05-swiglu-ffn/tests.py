"""
pytest data/app_data/05-transformers-llm/01-transformer-block/05-swiglu-ffn/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"05-transformers-llm/01-transformer-block/{Path(__file__).resolve().parent.name}")
swiglu_ffn = _module.swiglu_ffn

linear_forward = load_solution("03-dl-training/02-layers/01-linear-forward").linear_forward
swish_forward = load_solution("02-deep-learning-core/02-activations/06-swish").swish_forward


def test_output_shape_matches_input_d_model():
    rng = np.random.RandomState(0)
    d_model, d_ff = 8, 20
    x = rng.randn(2, 5, d_model)
    weight_gate = rng.randn(d_ff, d_model)
    weight_up = rng.randn(d_ff, d_model)
    weight_down = rng.randn(d_model, d_ff)
    result = swiglu_ffn(x, weight_gate, weight_up, weight_down)
    assert result.shape == (2, 5, d_model)


def test_matches_manual_composition_of_gate_and_up_branches():
    rng = np.random.RandomState(1)
    d_model, d_ff = 4, 12
    x = rng.randn(3, d_model)
    weight_gate = rng.randn(d_ff, d_model)
    weight_up = rng.randn(d_ff, d_model)
    weight_down = rng.randn(d_model, d_ff)

    zero_ff = np.zeros(d_ff)
    zero_model = np.zeros(d_model)
    gate = swish_forward(linear_forward(x, weight_gate, zero_ff))
    up = linear_forward(x, weight_up, zero_ff)
    expected = linear_forward(gate * up, weight_down, zero_model)

    result = swiglu_ffn(x, weight_gate, weight_up, weight_down)
    assert np.allclose(result, expected, atol=1e-8)


def test_zero_up_projection_weights_gives_zero_output():
    # up branch is 0 everywhere -> gate * up is 0 everywhere -> output is 0,
    # regardless of the gate branch's weights.
    rng = np.random.RandomState(2)
    d_model, d_ff = 4, 8
    x = rng.randn(2, d_model)
    weight_gate = rng.randn(d_ff, d_model)
    weight_up = np.zeros((d_ff, d_model))
    weight_down = rng.randn(d_model, d_ff)
    result = swiglu_ffn(x, weight_gate, weight_up, weight_down)
    assert np.allclose(result, 0.0, atol=1e-8)


def test_gate_and_up_use_separate_weight_matrices_not_the_same_one():
    # Directly targets a mutant that reuses weight_gate for BOTH branches
    # (or weight_up for both), which silently drops one of the two
    # distinct projections SwiGLU actually needs.
    rng = np.random.RandomState(3)
    d_model, d_ff = 4, 8
    x = rng.randn(2, d_model)
    weight_gate = rng.randn(d_ff, d_model)
    weight_up = rng.randn(d_ff, d_model)
    weight_down = rng.randn(d_model, d_ff)

    result = swiglu_ffn(x, weight_gate, weight_up, weight_down)
    result_same_weight = swiglu_ffn(x, weight_gate, weight_gate, weight_down)
    assert not np.allclose(result, result_same_weight, atol=1e-4)


def test_combination_is_elementwise_multiplication_not_addition():
    # Directly targets a mutant that adds the gate and up branches
    # together instead of multiplying them, which is a genuinely
    # different (and non-gating) operation.
    rng = np.random.RandomState(4)
    d_model, d_ff = 4, 8
    x = rng.randn(2, d_model)
    weight_gate = rng.randn(d_ff, d_model)
    weight_up = rng.randn(d_ff, d_model)
    weight_down = rng.randn(d_model, d_ff)

    result = swiglu_ffn(x, weight_gate, weight_up, weight_down)

    zero_ff = np.zeros(d_ff)
    zero_model = np.zeros(d_model)
    gate = swish_forward(linear_forward(x, weight_gate, zero_ff))
    up = linear_forward(x, weight_up, zero_ff)
    added_instead = linear_forward(gate + up, weight_down, zero_model)
    assert not np.allclose(result, added_instead, atol=1e-4)


def test_gate_branch_uses_swish_not_left_purely_linear():
    # Directly targets a mutant that skips the Swish activation on the
    # gate branch (leaving both branches purely linear, which collapses
    # the "gating" behavior into an ordinary bilinear product).
    rng = np.random.RandomState(5)
    d_model, d_ff = 4, 8
    x = rng.randn(2, d_model)
    weight_gate = rng.randn(d_ff, d_model)
    weight_up = rng.randn(d_ff, d_model)
    weight_down = rng.randn(d_model, d_ff)

    result = swiglu_ffn(x, weight_gate, weight_up, weight_down)

    zero_ff = np.zeros(d_ff)
    zero_model = np.zeros(d_model)
    ungated = linear_forward(x, weight_gate, zero_ff)
    up = linear_forward(x, weight_up, zero_ff)
    no_swish = linear_forward(ungated * up, weight_down, zero_model)
    assert not np.allclose(result, no_swish, atol=1e-4)
