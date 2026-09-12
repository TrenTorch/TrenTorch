"""
pytest data/app_data/05-transformers-llm/04-llm-engineering/03-capstone-tiny-llm/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"05-transformers-llm/04-llm-engineering/{Path(__file__).resolve().parent.name}")
build_char_vocab = _module.build_char_vocab
encode_char_text = _module.encode_char_text
decode_char_ids = _module.decode_char_ids
init_tiny_lm_params = _module.init_tiny_lm_params
train_tiny_char_lm = _module.train_tiny_char_lm

CORPUS = "the cat sat on the mat. the cat ran."


def test_build_char_vocab_contains_every_character_in_the_corpus():
    vocab = build_char_vocab(CORPUS)
    for ch in set(CORPUS):
        assert ch in vocab


def test_encode_decode_char_roundtrip():
    vocab = build_char_vocab(CORPUS)
    ids = encode_char_text(CORPUS, vocab)
    decoded = decode_char_ids(ids, vocab)
    assert decoded == CORPUS


def test_init_tiny_lm_params_shapes():
    vocab_size, d_model, d_ff, num_blocks = 20, 8, 16, 2
    embedding_table, blocks_params, output_weight = init_tiny_lm_params(vocab_size, d_model, d_ff, num_blocks, seed=0)
    assert embedding_table.shape == (vocab_size, d_model)
    assert len(blocks_params) == num_blocks
    assert output_weight.shape == (vocab_size, d_model)
    for params in blocks_params:
        assert params["weight_o"].shape == (d_model, d_model)
        assert params["ffn_weight1"].shape == (d_ff, d_model)


def test_init_tiny_lm_params_is_deterministic_given_a_seed():
    a = init_tiny_lm_params(10, 8, 16, 2, seed=42)
    b = init_tiny_lm_params(10, 8, 16, 2, seed=42)
    assert np.array_equal(a[0], b[0])
    assert np.array_equal(a[2], b[2])


def test_full_pipeline_runs_and_returns_expected_keys():
    result = train_tiny_char_lm(
        CORPUS, d_model=8, d_ff=16, num_heads=2, num_blocks=1, lr=0.5, num_steps=20, num_generated_chars=10, seed=0
    )
    assert set(result.keys()) == {"vocab", "loss_history", "trained_output_weight", "generated_text"}
    assert len(result["loss_history"]) == 20
    assert len(result["generated_text"]) == len(CORPUS) + 10


def test_training_loss_decreases_over_the_capstone_run():
    result = train_tiny_char_lm(
        CORPUS, d_model=8, d_ff=16, num_heads=2, num_blocks=1, lr=0.5, num_steps=30, num_generated_chars=5, seed=1
    )
    loss_history = result["loss_history"]
    assert loss_history[-1] < loss_history[0]


def test_generated_text_uses_only_characters_from_the_learned_vocabulary():
    result = train_tiny_char_lm(
        CORPUS, d_model=8, d_ff=16, num_heads=2, num_blocks=1, lr=0.3, num_steps=10, num_generated_chars=15, seed=2
    )
    vocab_chars = set(result["vocab"].keys())
    for ch in result["generated_text"]:
        assert ch in vocab_chars


def test_pipeline_is_deterministic_given_the_same_seed():
    result_a = train_tiny_char_lm(
        CORPUS, d_model=8, d_ff=16, num_heads=2, num_blocks=1, lr=0.5, num_steps=10, num_generated_chars=8, seed=3
    )
    result_b = train_tiny_char_lm(
        CORPUS, d_model=8, d_ff=16, num_heads=2, num_blocks=1, lr=0.5, num_steps=10, num_generated_chars=8, seed=3
    )
    assert result_a["generated_text"] == result_b["generated_text"]
    assert result_a["loss_history"] == result_b["loss_history"]
