"""
pytest data/app_data/04-seq-modeling/03-recurrent-neural-networks/07-seq2seq-bottleneck/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"04-seq-modeling/03-recurrent-neural-networks/{Path(__file__).resolve().parent.name}")
encode_all_hidden_states = _module.encode_all_hidden_states
get_bottleneck_context = _module.get_bottleneck_context
cosine_similarity = _module.cosine_similarity


def _weights(input_size, hidden_size, rng, scale=0.5):
    return (
        rng.randn(hidden_size, input_size) * scale,
        rng.randn(hidden_size, hidden_size) * scale,
        np.zeros(hidden_size),
        np.zeros(hidden_size),
    )


def test_encode_all_hidden_states_shape():
    rng = np.random.RandomState(0)
    seq_len, batch_size, input_size, hidden_size = 6, 2, 3, 4
    x_seq = rng.randn(seq_len, batch_size, input_size)
    weight_ih, weight_hh, bias_ih, bias_hh = _weights(input_size, hidden_size, rng)
    h0 = np.zeros((batch_size, hidden_size))
    result = encode_all_hidden_states(x_seq, h0, weight_ih, weight_hh, bias_ih, bias_hh)
    assert result.shape == (seq_len, batch_size, hidden_size)


def test_get_bottleneck_context_returns_the_last_time_step():
    hidden_states = np.array([[[1.0, 1.0]], [[2.0, 2.0]], [[3.0, 3.0]]])
    context = get_bottleneck_context(hidden_states)
    assert np.allclose(context, [[3.0, 3.0]])


def test_cosine_similarity_of_identical_vectors_is_one():
    a = np.array([1.0, 2.0, 3.0])
    assert np.isclose(cosine_similarity(a, a), 1.0)


def test_cosine_similarity_of_orthogonal_vectors_is_zero():
    a = np.array([1.0, 0.0])
    b = np.array([0.0, 1.0])
    assert np.isclose(cosine_similarity(a, b), 0.0, atol=1e-6)


def test_cosine_similarity_of_opposite_vectors_is_minus_one():
    a = np.array([1.0, 2.0])
    b = np.array([-1.0, -2.0])
    assert np.isclose(cosine_similarity(a, b), -1.0)


def test_bottleneck_context_is_barely_affected_by_early_differences_late_agreement():
    rng = np.random.RandomState(0)
    input_size, hidden_size, seq_len = 4, 6, 12
    weight_ih, weight_hh, bias_ih, bias_hh = _weights(input_size, hidden_size, rng)
    h0 = np.zeros((1, hidden_size))

    base = rng.randn(seq_len, 1, input_size)
    seq_a = base.copy()
    seq_b = base.copy()
    seq_b[:3] = rng.randn(3, 1, input_size) * 5  # very different early content, same late content

    ctx_a = get_bottleneck_context(encode_all_hidden_states(seq_a, h0, weight_ih, weight_hh, bias_ih, bias_hh))
    ctx_b = get_bottleneck_context(encode_all_hidden_states(seq_b, h0, weight_ih, weight_hh, bias_ih, bias_hh))
    sim = cosine_similarity(ctx_a, ctx_b)
    assert sim > 0.99


def test_bottleneck_context_is_strongly_affected_by_late_differences():
    rng = np.random.RandomState(0)
    input_size, hidden_size, seq_len = 4, 6, 12
    weight_ih, weight_hh, bias_ih, bias_hh = _weights(input_size, hidden_size, rng)
    h0 = np.zeros((1, hidden_size))

    base = rng.randn(seq_len, 1, input_size)
    seq_c = base.copy()
    seq_d = base.copy()
    seq_d[-3:] = rng.randn(3, 1, input_size) * 5  # same early content, very different late content

    ctx_c = get_bottleneck_context(encode_all_hidden_states(seq_c, h0, weight_ih, weight_hh, bias_ih, bias_hh))
    ctx_d = get_bottleneck_context(encode_all_hidden_states(seq_d, h0, weight_ih, weight_hh, bias_ih, bias_hh))
    sim = cosine_similarity(ctx_c, ctx_d)
    assert sim < 0.5


def test_early_information_is_far_better_preserved_in_the_full_hidden_state_history():
    # Directly demonstrates the ATTENTION fix's premise: even though the
    # BOTTLENECKED final context vector barely reflects early differences
    # (previous test), the FULL hidden state at the position where the
    # early difference actually occurred DOES clearly reflect it, proving
    # the information wasn't lost by the encoder itself, only by
    # discarding everything except the last step.
    rng = np.random.RandomState(0)
    input_size, hidden_size, seq_len = 4, 6, 12
    weight_ih, weight_hh, bias_ih, bias_hh = _weights(input_size, hidden_size, rng)
    h0 = np.zeros((1, hidden_size))

    base = rng.randn(seq_len, 1, input_size)
    seq_a = base.copy()
    seq_b = base.copy()
    seq_b[:3] = rng.randn(3, 1, input_size) * 5

    hs_a = encode_all_hidden_states(seq_a, h0, weight_ih, weight_hh, bias_ih, bias_hh)
    hs_b = encode_all_hidden_states(seq_b, h0, weight_ih, weight_hh, bias_ih, bias_hh)

    sim_at_step_2 = cosine_similarity(hs_a[2], hs_b[2])  # right after the early difference
    sim_at_final = cosine_similarity(hs_a[-1], hs_b[-1])  # the bottlenecked context
    assert sim_at_step_2 < sim_at_final
