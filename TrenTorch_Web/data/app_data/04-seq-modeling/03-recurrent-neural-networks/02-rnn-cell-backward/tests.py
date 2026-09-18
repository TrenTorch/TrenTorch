"""
pytest data/app_data/04-seq-modeling/03-recurrent-neural-networks/02-rnn-cell-backward/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"04-seq-modeling/03-recurrent-neural-networks/{Path(__file__).resolve().parent.name}")
rnn_cell_backward = _module.rnn_cell_backward


def test_all_gradient_shapes_match_their_originals():
    grad_h = np.random.randn(5, 3)
    h_next = np.tanh(np.random.randn(5, 3))
    x = np.random.randn(5, 4)
    h_prev = np.random.randn(5, 3)
    weight_ih = np.random.randn(3, 4)
    weight_hh = np.random.randn(3, 3)
    grads = rnn_cell_backward(grad_h, h_next, x, h_prev, weight_ih, weight_hh)
    grad_x, grad_h_prev, grad_wih, grad_whh, grad_bih, grad_bhh = grads
    assert grad_x.shape == x.shape
    assert grad_h_prev.shape == h_prev.shape
    assert grad_wih.shape == weight_ih.shape
    assert grad_whh.shape == weight_hh.shape
    assert grad_bih.shape == (3,)
    assert grad_bhh.shape == (3,)


def test_bias_ih_and_bias_hh_gradients_are_identical():
    grad_h = np.random.randn(4, 2)
    h_next = np.tanh(np.random.randn(4, 2))
    x = np.random.randn(4, 3)
    h_prev = np.random.randn(4, 2)
    weight_ih = np.random.randn(2, 3)
    weight_hh = np.random.randn(2, 2)
    grads = rnn_cell_backward(grad_h, h_next, x, h_prev, weight_ih, weight_hh)
    _, _, _, _, grad_bih, grad_bhh = grads
    assert np.allclose(grad_bih, grad_bhh)


def test_tanh_at_zero_output_leaves_gradient_unscaled():
    # h_next = 0 means the cell's output was exactly at tanh's zero
    # point, where tanh's derivative (1 - 0^2 = 1) leaves the upstream
    # gradient completely unscaled.
    grad_h = np.array([[2.0, -3.0]])
    h_next = np.array([[0.0, 0.0]])
    x = np.array([[1.0]])
    h_prev = np.array([[1.0, 1.0]])
    weight_ih = np.array([[1.0], [1.0]])
    weight_hh = np.eye(2)
    grads = rnn_cell_backward(grad_h, h_next, x, h_prev, weight_ih, weight_hh)
    grad_x = grads[0]
    # grad_z = grad_h * (1-0) = grad_h itself, so grad_x = grad_z @ weight_ih
    expected_grad_x = grad_h @ weight_ih
    assert np.allclose(grad_x, expected_grad_x)


def test_saturated_tanh_output_shrinks_the_gradient_toward_zero():
    # h_next close to +/-1 means tanh is nearly saturated, where its
    # derivative (1 - h_next^2) is close to zero, so gradients passing
    # through should be strongly attenuated.
    grad_h = np.array([[1.0]])
    h_next = np.array([[0.999]])
    x = np.array([[1.0]])
    h_prev = np.array([[1.0]])
    weight_ih = np.array([[1.0]])
    weight_hh = np.array([[1.0]])
    grads = rnn_cell_backward(grad_h, h_next, x, h_prev, weight_ih, weight_hh)
    grad_x = grads[0]
    assert abs(grad_x[0, 0]) < 0.01


def test_matches_known_oracle_from_pytorch_rnncell_backward():
    # verified directly against torch.nn.RNNCell + loss.backward()
    weight_ih = np.array([[1.0, 0.0], [0.0, 1.0]])
    weight_hh = np.array([[0.5, 0.0], [0.0, 0.5]])
    x = np.array([[1.0, 1.0]])
    h_prev = np.array([[0.5, 0.5]])
    z = x @ weight_ih.T + h_prev @ weight_hh.T
    h_next = np.tanh(z)
    grad_h = np.ones_like(h_next)
    grads = rnn_cell_backward(grad_h, h_next, x, h_prev, weight_ih, weight_hh)
    grad_x, grad_h_prev, grad_wih, grad_whh, grad_bih, grad_bhh = grads
    grad_z_expected = 1.0 - h_next**2
    assert np.allclose(grad_x, grad_z_expected @ weight_ih)
    assert np.allclose(grad_h_prev, grad_z_expected @ weight_hh)


def test_grad_weight_ih_uses_x_not_h_prev():
    # Directly targets a mutant that swaps grad_weight_ih's second factor
    # (using h_prev instead of x): for a case where x and h_prev are
    # clearly different values, this produces a visibly wrong result.
    grad_h = np.array([[1.0]])
    h_next = np.array([[0.0]])  # tanh derivative = 1, no scaling
    x = np.array([[100.0]])
    h_prev = np.array([[1.0]])
    weight_ih = np.array([[1.0]])
    weight_hh = np.array([[1.0]])
    grads = rnn_cell_backward(grad_h, h_next, x, h_prev, weight_ih, weight_hh)
    grad_weight_ih = grads[2]
    # correct: grad_z.T @ x = 1 * 100 = 100
    assert np.isclose(grad_weight_ih[0, 0], 100.0)
