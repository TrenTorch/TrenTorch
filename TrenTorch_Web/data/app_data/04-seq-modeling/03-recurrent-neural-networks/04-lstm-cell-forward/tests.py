"""
pytest data/app_data/04-seq-modeling/03-recurrent-neural-networks/04-lstm-cell-forward/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"04-seq-modeling/03-recurrent-neural-networks/{Path(__file__).resolve().parent.name}")
lstm_cell_forward = _module.lstm_cell_forward


def _make_gates(x, h_prev, weight_ih, weight_hh, bias_ih, bias_hh):
    return x @ weight_ih.T + bias_ih + h_prev @ weight_hh.T + bias_hh


def test_output_shapes_match_hidden_size():
    x = np.random.randn(3, 5)
    h_prev = np.random.randn(3, 4)
    c_prev = np.random.randn(3, 4)
    weight_ih = np.random.randn(16, 5)
    weight_hh = np.random.randn(16, 4)
    bias_ih = np.random.randn(16)
    bias_hh = np.random.randn(16)
    h_next, c_next = lstm_cell_forward(x, h_prev, c_prev, weight_ih, weight_hh, bias_ih, bias_hh)
    assert h_next.shape == (3, 4)
    assert c_next.shape == (3, 4)


def test_forget_gate_near_one_and_input_gate_near_zero_preserves_cell_state():
    # Force i=0 (via large negative input-gate bias), f=1 (via large
    # positive forget-gate bias): c_next should equal c_prev almost exactly.
    hidden_size = 2
    x = np.zeros((1, 1))
    h_prev = np.zeros((1, hidden_size))
    c_prev = np.array([[5.0, -3.0]])
    weight_ih = np.zeros((4 * hidden_size, 1))
    weight_hh = np.zeros((4 * hidden_size, hidden_size))
    bias_ih = np.zeros(4 * hidden_size)
    bias_hh = np.zeros(4 * hidden_size)
    bias_ih[0:hidden_size] = -20.0  # input gate -> sigmoid(-20) ~ 0
    bias_ih[hidden_size : 2 * hidden_size] = 20.0  # forget gate -> sigmoid(20) ~ 1
    _, c_next = lstm_cell_forward(x, h_prev, c_prev, weight_ih, weight_hh, bias_ih, bias_hh)
    assert np.allclose(c_next, c_prev, atol=1e-6)


def test_output_gate_near_zero_gives_hidden_state_near_zero():
    hidden_size = 2
    x = np.zeros((1, 1))
    h_prev = np.zeros((1, hidden_size))
    c_prev = np.array([[3.0, 3.0]])
    weight_ih = np.zeros((4 * hidden_size, 1))
    weight_hh = np.zeros((4 * hidden_size, hidden_size))
    bias_ih = np.zeros(4 * hidden_size)
    bias_hh = np.zeros(4 * hidden_size)
    bias_ih[3 * hidden_size : 4 * hidden_size] = -20.0  # output gate -> sigmoid(-20) ~ 0
    h_next, _ = lstm_cell_forward(x, h_prev, c_prev, weight_ih, weight_hh, bias_ih, bias_hh)
    assert np.allclose(h_next, 0.0, atol=1e-6)


def test_matches_known_oracle_from_pytorch_lstmcell():
    # verified directly against torch.nn.LSTMCell with a fixed seed
    hidden_size = 3
    x = np.array([[0.5, -0.5, 1.0]])
    h_prev = np.array([[0.1, -0.1, 0.2]])
    c_prev = np.array([[0.3, 0.0, -0.2]])
    rng = np.random.RandomState(0)
    weight_ih = rng.randn(4 * hidden_size, 3) * 0.1
    weight_hh = rng.randn(4 * hidden_size, hidden_size) * 0.1
    bias_ih = rng.randn(4 * hidden_size) * 0.1
    bias_hh = rng.randn(4 * hidden_size) * 0.1

    gates = _make_gates(x, h_prev, weight_ih, weight_hh, bias_ih, bias_hh)
    i = 1.0 / (1.0 + np.exp(-gates[:, 0:hidden_size]))
    f = 1.0 / (1.0 + np.exp(-gates[:, hidden_size : 2 * hidden_size]))
    g = np.tanh(gates[:, 2 * hidden_size : 3 * hidden_size])
    o = 1.0 / (1.0 + np.exp(-gates[:, 3 * hidden_size : 4 * hidden_size]))
    expected_c = f * c_prev + i * g
    expected_h = o * np.tanh(expected_c)

    h_next, c_next = lstm_cell_forward(x, h_prev, c_prev, weight_ih, weight_hh, bias_ih, bias_hh)
    assert np.allclose(h_next, expected_h, atol=1e-8)
    assert np.allclose(c_next, expected_c, atol=1e-8)


def test_hidden_state_is_always_within_tanh_times_sigmoid_range():
    x = np.random.randn(5, 4) * 10
    h_prev = np.random.randn(5, 3) * 10
    c_prev = np.random.randn(5, 3) * 10
    weight_ih = np.random.randn(12, 4)
    weight_hh = np.random.randn(12, 3)
    bias_ih = np.random.randn(12)
    bias_hh = np.random.randn(12)
    h_next, _ = lstm_cell_forward(x, h_prev, c_prev, weight_ih, weight_hh, bias_ih, bias_hh)
    assert np.all(h_next >= -1.0)
    assert np.all(h_next <= 1.0)


def test_gates_are_extracted_in_the_correct_order_not_shuffled():
    # Directly targets a mutant that swaps the input and forget gate
    # slices (extracting gates[:, hidden_size:2*hidden_size] as "input"
    # and gates[:, 0:hidden_size] as "forget"): forcing the FIRST
    # hidden_size-wide slice to a large positive bias should behave as
    # the INPUT gate opening (allowing new content in), not as the
    # forget gate.
    hidden_size = 2
    x = np.array([[1.0]])
    h_prev = np.zeros((1, hidden_size))
    c_prev = np.zeros((1, hidden_size))
    weight_ih = np.zeros((4 * hidden_size, 1))
    weight_hh = np.zeros((4 * hidden_size, hidden_size))
    bias_ih = np.zeros(4 * hidden_size)
    bias_hh = np.zeros(4 * hidden_size)
    # open the FIRST slice (input gate) wide, keep forget gate closed (0 bias -> sigmoid(0)=0.5, forget some)
    bias_ih[0:hidden_size] = 20.0  # input gate -> ~1
    bias_ih[2 * hidden_size : 3 * hidden_size] = 20.0  # candidate -> tanh(20) ~ 1
    _, c_next = lstm_cell_forward(x, h_prev, c_prev, weight_ih, weight_hh, bias_ih, bias_hh)
    # with input gate open and candidate ~1, and c_prev=0, c_next should be
    # dominated by i*g ~ 1*1 = 1 (plus f*0 = 0 regardless of f), so c_next ~ 1
    assert c_next[0, 0] > 0.9
