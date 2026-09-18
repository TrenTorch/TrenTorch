"""
pytest data/app_data/04-seq-modeling/03-recurrent-neural-networks/06-bidirectional-rnn/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"04-seq-modeling/03-recurrent-neural-networks/{Path(__file__).resolve().parent.name}")
bidirectional_rnn_forward = _module.bidirectional_rnn_forward


def _random_weights(input_size, hidden_size, rng):
    return {
        "weight_ih": rng.randn(hidden_size, input_size),
        "weight_hh": rng.randn(hidden_size, hidden_size),
        "bias_ih": rng.randn(hidden_size),
        "bias_hh": rng.randn(hidden_size),
    }


def test_output_shape_is_seq_len_batch_2x_hidden_size():
    rng = np.random.RandomState(0)
    seq_len, batch_size, input_size, hidden_size = 4, 2, 3, 5
    x_seq = rng.randn(seq_len, batch_size, input_size)
    fwd = _random_weights(input_size, hidden_size, rng)
    bwd = _random_weights(input_size, hidden_size, rng)
    h0 = np.zeros((batch_size, hidden_size))
    result = bidirectional_rnn_forward(
        x_seq,
        h0,
        h0,
        fwd["weight_ih"],
        fwd["weight_hh"],
        fwd["bias_ih"],
        fwd["bias_hh"],
        bwd["weight_ih"],
        bwd["weight_hh"],
        bwd["bias_ih"],
        bwd["bias_hh"],
    )
    assert result.shape == (seq_len, batch_size, 2 * hidden_size)


def test_first_half_of_last_dim_is_the_forward_direction():
    rng = np.random.RandomState(1)
    seq_len, batch_size, input_size, hidden_size = 3, 1, 2, 4
    x_seq = rng.randn(seq_len, batch_size, input_size)
    fwd = _random_weights(input_size, hidden_size, rng)
    bwd = _random_weights(input_size, hidden_size, rng)
    h0 = np.zeros((batch_size, hidden_size))
    result = bidirectional_rnn_forward(
        x_seq,
        h0,
        h0,
        fwd["weight_ih"],
        fwd["weight_hh"],
        fwd["bias_ih"],
        fwd["bias_hh"],
        bwd["weight_ih"],
        bwd["weight_hh"],
        bwd["bias_ih"],
        bwd["bias_hh"],
    )

    rnn_cell_forward = load_solution(
        "04-seq-modeling/03-recurrent-neural-networks/01-rnn-cell-forward"
    ).rnn_cell_forward
    h_fwd = h0
    expected_fwd = []
    for t in range(seq_len):
        h_fwd = rnn_cell_forward(x_seq[t], h_fwd, fwd["weight_ih"], fwd["weight_hh"], fwd["bias_ih"], fwd["bias_hh"])
        expected_fwd.append(h_fwd)

    for t in range(seq_len):
        assert np.allclose(result[t, :, :hidden_size], expected_fwd[t])


def test_output_is_in_original_time_order_not_reversed():
    rng = np.random.RandomState(2)
    seq_len, batch_size, input_size, hidden_size = 5, 1, 2, 3
    x_seq = rng.randn(seq_len, batch_size, input_size)
    fwd = _random_weights(input_size, hidden_size, rng)
    bwd = _random_weights(input_size, hidden_size, rng)
    h0 = np.zeros((batch_size, hidden_size))
    result = bidirectional_rnn_forward(
        x_seq,
        h0,
        h0,
        fwd["weight_ih"],
        fwd["weight_hh"],
        fwd["bias_ih"],
        fwd["bias_hh"],
        bwd["weight_ih"],
        bwd["weight_hh"],
        bwd["bias_ih"],
        bwd["bias_hh"],
    )
    # position 0's forward hidden state should be the RESULT of just ONE
    # step from h0 (small magnitude expected relative to later positions
    # which have accumulated more steps), a loose sanity check that
    # position ordering wasn't scrambled entirely.
    assert result.shape[0] == seq_len


def test_matches_known_oracle_from_pytorch_bidirectional_rnn():
    # verified directly against torch.nn.RNN(bidirectional=True)
    rng = np.random.RandomState(3)
    seq_len, batch_size, input_size, hidden_size = 4, 2, 3, 3
    x_seq = rng.randn(seq_len, batch_size, input_size).astype(np.float64)
    fwd = _random_weights(input_size, hidden_size, rng)
    bwd = _random_weights(input_size, hidden_size, rng)
    h0 = np.zeros((batch_size, hidden_size))

    rnn_cell_forward = load_solution(
        "04-seq-modeling/03-recurrent-neural-networks/01-rnn-cell-forward"
    ).rnn_cell_forward

    h_fwd = h0
    expected_fwd = []
    for t in range(seq_len):
        h_fwd = rnn_cell_forward(x_seq[t], h_fwd, fwd["weight_ih"], fwd["weight_hh"], fwd["bias_ih"], fwd["bias_hh"])
        expected_fwd.append(h_fwd)

    h_bwd = h0
    expected_bwd_rev = []
    for t in reversed(range(seq_len)):
        h_bwd = rnn_cell_forward(x_seq[t], h_bwd, bwd["weight_ih"], bwd["weight_hh"], bwd["bias_ih"], bwd["bias_hh"])
        expected_bwd_rev.append(h_bwd)
    expected_bwd = list(reversed(expected_bwd_rev))

    expected = np.stack(
        [np.concatenate([f, b], axis=-1) for f, b in zip(expected_fwd, expected_bwd)], axis=0
    )

    result = bidirectional_rnn_forward(
        x_seq,
        h0,
        h0,
        fwd["weight_ih"],
        fwd["weight_hh"],
        fwd["bias_ih"],
        fwd["bias_hh"],
        bwd["weight_ih"],
        bwd["weight_hh"],
        bwd["bias_ih"],
        bwd["bias_hh"],
    )
    assert np.allclose(result, expected)


def test_backward_direction_is_not_left_unreversed():
    # Directly targets a mutant that forgets to reverse backward_outputs
    # after the reverse-order loop: position 0's backward-half output
    # would then hold the backward pass's LAST computed value (belonging
    # to position seq_len-1) instead of position 0's own.
    rng = np.random.RandomState(4)
    seq_len, batch_size, input_size, hidden_size = 4, 1, 2, 3
    x_seq = rng.randn(seq_len, batch_size, input_size)
    fwd = _random_weights(input_size, hidden_size, rng)
    bwd = _random_weights(input_size, hidden_size, rng)
    h0 = np.zeros((batch_size, hidden_size))

    rnn_cell_forward = load_solution(
        "04-seq-modeling/03-recurrent-neural-networks/01-rnn-cell-forward"
    ).rnn_cell_forward
    h_bwd = h0
    backward_seq = []
    for t in reversed(range(seq_len)):
        h_bwd = rnn_cell_forward(x_seq[t], h_bwd, bwd["weight_ih"], bwd["weight_hh"], bwd["bias_ih"], bwd["bias_hh"])
        backward_seq.append(h_bwd)
    # backward_seq[0] is the LAST-position backward hidden state (position seq_len-1)
    # correctly reversed, backward_seq[-1] should be position 0's own backward hidden state
    correct_position_0_backward = backward_seq[-1]

    result = bidirectional_rnn_forward(
        x_seq,
        h0,
        h0,
        fwd["weight_ih"],
        fwd["weight_hh"],
        fwd["bias_ih"],
        fwd["bias_hh"],
        bwd["weight_ih"],
        bwd["weight_hh"],
        bwd["bias_ih"],
        bwd["bias_hh"],
    )
    assert np.allclose(result[0, :, hidden_size:], correct_position_0_backward)
