"""
pytest data/app_data/05-transformers-llm/04-llm-engineering/02-speculative-decoding/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"05-transformers-llm/04-llm-engineering/{Path(__file__).resolve().parent.name}")
speculative_decode_step = _module.speculative_decode_step

greedy_decode = load_solution("05-transformers-llm/03-language-model-assembly/07-greedy-decoding").greedy_decode


def test_identical_draft_and_target_models_accept_every_drafted_token():
    # When the draft and target models are literally the same model, the
    # target must always agree with the draft's own greedy choices, so
    # every drafted token should be accepted.
    rng = np.random.RandomState(0)
    vocab_size, d_model, num_heads, seq_len = 10, 4, 2, 3
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    embedding_table = rng.randn(vocab_size, d_model)

    accepted, num_accepted = speculative_decode_step(
        token_ids,
        embedding_table, [], num_heads, True, None,
        embedding_table, [], num_heads, True, None,
        num_draft_tokens=4,
    )
    assert num_accepted == 4
    assert accepted.shape == (1, seq_len + 4)


def test_identical_models_match_running_greedy_decode_directly():
    rng = np.random.RandomState(1)
    vocab_size, d_model, num_heads, seq_len = 10, 4, 2, 3
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    embedding_table = rng.randn(vocab_size, d_model)

    accepted, _ = speculative_decode_step(
        token_ids,
        embedding_table, [], num_heads, True, None,
        embedding_table, [], num_heads, True, None,
        num_draft_tokens=5,
    )
    direct_greedy = greedy_decode(token_ids, embedding_table, [], num_heads, True, None, num_new_tokens=5)
    assert np.array_equal(accepted, direct_greedy)


def test_disagreeing_models_reject_at_the_first_mismatch():
    # Construct a draft model that always proposes token 0, and a target
    # model that always prefers token 3 (disagreeing immediately), so
    # exactly 0 tokens should be accepted, and the single corrected token
    # appended must be the TARGET's choice (3), not the draft's (0).
    vocab_size, d_model, num_heads, seq_len = 5, 1, 1, 2
    token_ids = np.array([[1, 2]])
    embedding_table = np.full((vocab_size, d_model), 100.0)

    draft_output_weight = np.full((vocab_size, d_model), -1.0)
    draft_output_weight[0] = 1.0  # draft always predicts token 0

    target_output_weight = np.full((vocab_size, d_model), -1.0)
    target_output_weight[3] = 1.0  # target always predicts token 3

    accepted, num_accepted = speculative_decode_step(
        token_ids,
        embedding_table, [], num_heads, False, draft_output_weight,
        embedding_table, [], num_heads, False, target_output_weight,
        num_draft_tokens=3,
    )
    assert num_accepted == 0
    assert accepted.shape == (1, seq_len + 1)
    assert accepted[0, -1] == 3  # corrected to the target's own choice


def test_original_prefix_is_always_preserved():
    rng = np.random.RandomState(2)
    vocab_size, d_model, num_heads, seq_len = 8, 4, 2, 4
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    embedding_table = rng.randn(vocab_size, d_model)

    accepted, _ = speculative_decode_step(
        token_ids,
        embedding_table, [], num_heads, True, None,
        embedding_table, [], num_heads, True, None,
        num_draft_tokens=3,
    )
    assert np.array_equal(accepted[:, :seq_len], token_ids)


def test_num_accepted_never_exceeds_num_draft_tokens():
    rng = np.random.RandomState(3)
    vocab_size, d_model, num_heads, seq_len = 6, 4, 2, 3
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    draft_embedding = rng.randn(vocab_size, d_model)
    target_embedding = rng.randn(vocab_size, d_model)  # a genuinely different, unrelated model

    _, num_accepted = speculative_decode_step(
        token_ids,
        draft_embedding, [], num_heads, True, None,
        target_embedding, [], num_heads, True, None,
        num_draft_tokens=5,
    )
    assert 0 <= num_accepted <= 5
