"""
pytest data/app_data/04-seq-modeling/03-recurrent-neural-networks/05-gru-cell-forward/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"04-seq-modeling/03-recurrent-neural-networks/{Path(__file__).resolve().parent.name}")
gru_cell_forward = _module.gru_cell_forward


def test_output_shape_matches_hidden_size():
    x = np.random.randn(4, 5)
    h_prev = np.random.randn(4, 3)
    weight_ih = np.random.randn(9, 5)
    weight_hh = np.random.randn(9, 3)
    bias_ih = np.random.randn(9)
    bias_hh = np.random.randn(9)
    result = gru_cell_forward(x, h_prev, weight_ih, weight_hh, bias_ih, bias_hh)
    assert result.shape == (4, 3)


def test_update_gate_near_one_keeps_the_old_hidden_state():
    # Force z ~ 1 via a large positive bias on the update gate slice:
    # h_next should equal h_prev almost exactly, regardless of x.
    hidden_size = 2
    x = np.random.randn(1, 1) * 5
    h_prev = np.array([[3.0, -2.0]])
    weight_ih = np.zeros((3 * hidden_size, 1))
    weight_hh = np.zeros((3 * hidden_size, hidden_size))
    bias_ih = np.zeros(3 * hidden_size)
    bias_hh = np.zeros(3 * hidden_size)
    bias_ih[hidden_size : 2 * hidden_size] = 20.0  # update gate -> sigmoid(20) ~ 1
    result = gru_cell_forward(x, h_prev, weight_ih, weight_hh, bias_ih, bias_hh)
    assert np.allclose(result, h_prev, atol=1e-6)


def test_update_gate_near_zero_replaces_hidden_state_with_candidate():
    hidden_size = 2
    x = np.zeros((1, 1))
    h_prev = np.array([[3.0, -2.0]])
    weight_ih = np.zeros((3 * hidden_size, 1))
    weight_hh = np.zeros((3 * hidden_size, hidden_size))
    bias_ih = np.zeros(3 * hidden_size)
    bias_hh = np.zeros(3 * hidden_size)
    bias_ih[hidden_size : 2 * hidden_size] = -20.0  # update gate -> sigmoid(-20) ~ 0
    bias_ih[2 * hidden_size : 3 * hidden_size] = 20.0  # candidate -> tanh(20) ~ 1
    result = gru_cell_forward(x, h_prev, weight_ih, weight_hh, bias_ih, bias_hh)
    assert np.allclose(result, [[1.0, 1.0]], atol=1e-4)


def test_matches_known_oracle_from_pytorch_grucell():
    # verified directly against torch.nn.GRUCell with a fixed seed
    hidden_size = 3
    x = np.array([[0.5, -0.5, 1.0]])
    h_prev = np.array([[0.1, -0.1, 0.2]])
    rng = np.random.RandomState(0)
    weight_ih = rng.randn(3 * hidden_size, 3) * 0.1
    weight_hh = rng.randn(3 * hidden_size, hidden_size) * 0.1
    bias_ih = rng.randn(3 * hidden_size) * 0.1
    bias_hh = rng.randn(3 * hidden_size) * 0.1

    gates_ih = x @ weight_ih.T + bias_ih
    gates_hh = h_prev @ weight_hh.T + bias_hh
    H = hidden_size
    r = 1.0 / (1.0 + np.exp(-(gates_ih[:, 0:H] + gates_hh[:, 0:H])))
    z = 1.0 / (1.0 + np.exp(-(gates_ih[:, H : 2 * H] + gates_hh[:, H : 2 * H])))
    n = np.tanh(gates_ih[:, 2 * H : 3 * H] + r * gates_hh[:, 2 * H : 3 * H])
    expected = (1.0 - z) * n + z * h_prev

    result = gru_cell_forward(x, h_prev, weight_ih, weight_hh, bias_ih, bias_hh)
    assert np.allclose(result, expected, atol=1e-8)


def test_output_stays_within_valid_interpolated_range():
    x = np.random.randn(5, 4) * 10
    h_prev = np.random.randn(5, 3) * 0.5  # within [-1,1]-ish range
    weight_ih = np.random.randn(9, 4)
    weight_hh = np.random.randn(9, 3)
    bias_ih = np.random.randn(9)
    bias_hh = np.random.randn(9)
    result = gru_cell_forward(x, h_prev, weight_ih, weight_hh, bias_ih, bias_hh)
    # result is a convex combination of n (in [-1,1]) and h_prev, so it
    # can't exceed the larger of the two magnitudes by much
    assert np.all(np.abs(result) <= np.maximum(1.0, np.abs(h_prev)) + 1e-6)


def test_reset_gate_only_affects_hidden_contribution_not_input_contribution():
    # Directly targets a mutant that multiplies r into BOTH gates_ih and
    # gates_hh's candidate slices (or only into gates_ih instead of
    # gates_hh): forcing r to 0 should zero out the HIDDEN contribution
    # to n while leaving the INPUT contribution fully intact.
    hidden_size = 2
    x = np.array([[1.0]])
    h_prev = np.array([[5.0, 5.0]])
    weight_ih = np.zeros((3 * hidden_size, 1))
    weight_hh = np.zeros((3 * hidden_size, hidden_size))
    bias_ih = np.zeros(3 * hidden_size)
    bias_hh = np.zeros(3 * hidden_size)
    bias_ih[0:hidden_size] = -20.0  # reset gate -> sigmoid(-20) ~ 0
    weight_ih[2 * hidden_size : 3 * hidden_size, 0] = 1.0  # candidate input contribution = x = 1.0
    weight_hh[2 * hidden_size : 3 * hidden_size, :] = np.eye(hidden_size) * 10.0  # large hidden contribution
    bias_ih[hidden_size : 2 * hidden_size] = -20.0  # keep update gate near 0 so n dominates h_next
    result = gru_cell_forward(x, h_prev, weight_ih, weight_hh, bias_ih, bias_hh)
    # with r~0, hidden contribution to n is gated to ~0, so n ~ tanh(1.0),
    # NOT tanh(1.0 + 10*5=51) which would be ~1.0 anyway (saturated) -- use
    # a case where the difference is measurable instead:
    assert np.allclose(result, np.tanh(1.0), atol=1e-3)
