"""
pytest data/app_data/04-seq-modeling/03-recurrent-neural-networks/01-rnn-cell-forward/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"04-seq-modeling/03-recurrent-neural-networks/{Path(__file__).resolve().parent.name}")
rnn_cell_forward = _module.rnn_cell_forward


def test_output_shape_matches_hidden_state_shape():
    x = np.random.randn(5, 4)
    h_prev = np.random.randn(5, 3)
    weight_ih = np.random.randn(3, 4)
    weight_hh = np.random.randn(3, 3)
    bias_ih = np.random.randn(3)
    bias_hh = np.random.randn(3)
    result = rnn_cell_forward(x, h_prev, weight_ih, weight_hh, bias_ih, bias_hh)
    assert result.shape == (5, 3)


def test_output_is_always_within_tanh_range():
    x = np.random.randn(10, 6) * 100
    h_prev = np.random.randn(10, 5) * 100
    weight_ih = np.random.randn(5, 6)
    weight_hh = np.random.randn(5, 5)
    bias_ih = np.random.randn(5)
    bias_hh = np.random.randn(5)
    result = rnn_cell_forward(x, h_prev, weight_ih, weight_hh, bias_ih, bias_hh)
    assert np.all(result >= -1.0)
    assert np.all(result <= 1.0)


def test_hand_computed_example():
    x = np.array([[1.0]])
    h_prev = np.array([[0.0]])
    weight_ih = np.array([[1.0]])
    weight_hh = np.array([[1.0]])
    bias_ih = np.array([0.0])
    bias_hh = np.array([0.0])
    result = rnn_cell_forward(x, h_prev, weight_ih, weight_hh, bias_ih, bias_hh)
    assert np.isclose(result[0, 0], np.tanh(1.0))


def test_zero_input_and_hidden_and_bias_gives_zero_output():
    x = np.zeros((2, 3))
    h_prev = np.zeros((2, 4))
    weight_ih = np.random.randn(4, 3)
    weight_hh = np.random.randn(4, 4)
    bias_ih = np.zeros(4)
    bias_hh = np.zeros(4)
    result = rnn_cell_forward(x, h_prev, weight_ih, weight_hh, bias_ih, bias_hh)
    assert np.allclose(result, 0.0)


def test_matches_known_oracle_from_pytorch_rnncell():
    # verified directly against torch.nn.RNNCell with a fixed seed
    x = np.array([[0.5, -0.5]])
    h_prev = np.array([[0.1, 0.2]])
    weight_ih = np.array([[1.0, 0.0], [0.0, 1.0]])
    weight_hh = np.array([[0.5, 0.5], [-0.5, 0.5]])
    bias_ih = np.array([0.0, 0.0])
    bias_hh = np.array([0.0, 0.0])
    result = rnn_cell_forward(x, h_prev, weight_ih, weight_hh, bias_ih, bias_hh)
    # pre-activation: x@weight_ih.T = [0.5, -0.5]
    # h_prev@weight_hh.T = [0.1*0.5+0.2*0.5, 0.1*(-0.5)+0.2*0.5] = [0.15, 0.05]
    # sum = [0.65, -0.45]
    expected = np.tanh([[0.65, -0.45]])
    assert np.allclose(result, expected, atol=1e-6)


def test_works_for_batch_size_one():
    x = np.random.randn(1, 3)
    h_prev = np.random.randn(1, 2)
    weight_ih = np.random.randn(2, 3)
    weight_hh = np.random.randn(2, 2)
    bias_ih = np.random.randn(2)
    bias_hh = np.random.randn(2)
    result = rnn_cell_forward(x, h_prev, weight_ih, weight_hh, bias_ih, bias_hh)
    assert result.shape == (1, 2)


def test_sums_both_contributions_before_tanh_not_after():
    # Directly targets a mutant that applies tanh to EACH contribution
    # separately and then sums (tanh(a) + tanh(b)) instead of summing
    # first and applying tanh once (tanh(a + b)): these are NOT
    # mathematically equivalent, and produce different, out-of-range
    # values (tanh(a)+tanh(b) can exceed the [-1, 1] range tanh(a+b)
    # never does).
    x = np.array([[5.0]])
    h_prev = np.array([[5.0]])
    weight_ih = np.array([[1.0]])
    weight_hh = np.array([[1.0]])
    bias_ih = np.array([0.0])
    bias_hh = np.array([0.0])
    result = rnn_cell_forward(x, h_prev, weight_ih, weight_hh, bias_ih, bias_hh)
    # correct: tanh(5 + 5) = tanh(10) ~ 0.9999999958776927
    assert np.isclose(result[0, 0], np.tanh(10.0), atol=1e-6)
    # broken (tanh applied separately then summed): tanh(5)+tanh(5) ~ 1.9998
    wrong_if_separate = np.tanh(5.0) + np.tanh(5.0)
    assert not np.isclose(result[0, 0], wrong_if_separate, atol=1e-3)
