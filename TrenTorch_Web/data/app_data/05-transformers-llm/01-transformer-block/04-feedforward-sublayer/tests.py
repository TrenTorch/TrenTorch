"""
pytest data/app_data/05-transformers-llm/01-transformer-block/04-feedforward-sublayer/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"05-transformers-llm/01-transformer-block/{Path(__file__).resolve().parent.name}")
feedforward_sublayer = _module.feedforward_sublayer

linear_forward = load_solution("03-dl-training/02-layers/01-linear-forward").linear_forward
gelu_forward = load_solution("02-deep-learning-core/02-activations/05-gelu").gelu_forward


def test_output_shape_matches_input_d_model_not_the_hidden_size():
    rng = np.random.RandomState(0)
    d_model, d_ff = 8, 32
    x = rng.randn(2, 5, d_model)
    weight1, bias1 = rng.randn(d_ff, d_model), rng.randn(d_ff)
    weight2, bias2 = rng.randn(d_model, d_ff), rng.randn(d_model)
    result = feedforward_sublayer(x, weight1, bias1, weight2, bias2)
    assert result.shape == (2, 5, d_model)


def test_matches_manual_composition_of_linear_forward_and_gelu():
    rng = np.random.RandomState(1)
    d_model, d_ff = 4, 16
    x = rng.randn(3, d_model)
    weight1, bias1 = rng.randn(d_ff, d_model), rng.randn(d_ff)
    weight2, bias2 = rng.randn(d_model, d_ff), rng.randn(d_model)

    result = feedforward_sublayer(x, weight1, bias1, weight2, bias2)
    manual_hidden = gelu_forward(linear_forward(x, weight1, bias1))
    manual_output = linear_forward(manual_hidden, weight2, bias2)
    assert np.allclose(result, manual_output, atol=1e-8)


def test_zero_second_layer_weights_gives_zero_output():
    rng = np.random.RandomState(2)
    d_model, d_ff = 4, 8
    x = rng.randn(2, d_model)
    weight1, bias1 = rng.randn(d_ff, d_model), rng.randn(d_ff)
    weight2, bias2 = np.zeros((d_model, d_ff)), np.zeros(d_model)
    result = feedforward_sublayer(x, weight1, bias1, weight2, bias2)
    assert np.allclose(result, 0.0, atol=1e-8)


def test_activation_is_applied_between_the_two_linear_layers_not_omitted():
    # Directly targets a mutant that drops GELU entirely, leaving two
    # composed linear layers (which would just be a single linear map).
    rng = np.random.RandomState(3)
    d_model, d_ff = 4, 8
    x = rng.randn(2, d_model)
    weight1, bias1 = rng.randn(d_ff, d_model), rng.randn(d_ff)
    weight2, bias2 = rng.randn(d_model, d_ff), rng.randn(d_model)

    result = feedforward_sublayer(x, weight1, bias1, weight2, bias2)
    purely_linear = linear_forward(linear_forward(x, weight1, bias1), weight2, bias2)
    assert not np.allclose(result, purely_linear, atol=1e-4)


def test_linear_input_produces_a_nonlinear_output_due_to_gelu():
    # Sanity check that the sublayer is not accidentally purely linear
    # (e.g. if GELU were dropped, two composed linear layers would still
    # just be one big linear map, and scaling x by 2 would scale the
    # output by exactly 2, which GELU's nonlinearity breaks).
    rng = np.random.RandomState(4)
    d_model, d_ff = 4, 8
    x = rng.randn(2, d_model)
    weight1, bias1 = rng.randn(d_ff, d_model), np.zeros(d_ff)
    weight2, bias2 = rng.randn(d_model, d_ff), np.zeros(d_model)

    out_x = feedforward_sublayer(x, weight1, bias1, weight2, bias2)
    out_2x = feedforward_sublayer(2.0 * x, weight1, bias1, weight2, bias2)
    assert not np.allclose(out_2x, 2.0 * out_x, atol=1e-3)
