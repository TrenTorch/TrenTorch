"""
pytest data/app_data/05-transformers-llm/03-language-model-assembly/08-temperature-topk-sampling/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"05-transformers-llm/03-language-model-assembly/{Path(__file__).resolve().parent.name}"
)
scale_and_filter_logits = _module.scale_and_filter_logits
sample_next_token = _module.sample_next_token
sample_decode = _module.sample_decode


def test_scale_and_filter_no_top_k_just_divides_by_temperature():
    logits = np.array([2.0, 4.0, 6.0])
    result = scale_and_filter_logits(logits, temperature=2.0, top_k=None)
    assert np.allclose(result, [1.0, 2.0, 3.0], atol=1e-10)


def test_top_k_keeps_only_the_k_highest_logits():
    logits = np.array([1.0, 5.0, 3.0, 4.0, 2.0])
    result = scale_and_filter_logits(logits, temperature=1.0, top_k=2)
    kept = np.isfinite(result)
    assert kept.sum() == 2
    # The two highest values (5.0 at index 1, 4.0 at index 3) must be kept.
    assert kept[1] and kept[3]
    assert not kept[0] and not kept[2] and not kept[4]


def test_top_k_none_keeps_everything_finite():
    logits = np.array([1.0, 5.0, 3.0])
    result = scale_and_filter_logits(logits, temperature=1.0, top_k=None)
    assert np.all(np.isfinite(result))


def test_top_k_larger_than_vocab_keeps_everything_finite():
    logits = np.array([1.0, 5.0, 3.0])
    result = scale_and_filter_logits(logits, temperature=1.0, top_k=10)
    assert np.all(np.isfinite(result))


def test_sample_next_token_always_returns_a_valid_index():
    rng = np.random.RandomState(0)
    logits = np.array([1.0, 2.0, 3.0, 0.5])
    for _ in range(20):
        token = sample_next_token(logits, temperature=1.0, top_k=None, rng=rng)
        assert 0 <= token < len(logits)


def test_top_k_one_is_equivalent_to_greedy_argmax():
    rng = np.random.RandomState(1)
    logits = np.array([1.0, 5.0, 3.0, 4.0, 2.0])
    for _ in range(10):
        token = sample_next_token(logits, temperature=1.0, top_k=1, rng=rng)
        assert token == np.argmax(logits)


def test_low_temperature_makes_sampling_nearly_deterministic():
    # A very low temperature sharpens the distribution close to one-hot,
    # so repeated samples should almost always return the argmax.
    rng = np.random.RandomState(2)
    logits = np.array([1.0, 5.0, 3.0])
    samples = [sample_next_token(logits, temperature=0.01, top_k=None, rng=rng) for _ in range(30)]
    assert samples.count(int(np.argmax(logits))) >= 28


def test_high_temperature_produces_varied_samples():
    # A very high (flattening) temperature should produce a genuine mix
    # of outcomes over many draws, not always the same token.
    rng = np.random.RandomState(3)
    logits = np.array([1.0, 1.1, 0.9, 1.05])
    samples = {sample_next_token(logits, temperature=10.0, top_k=None, rng=rng) for _ in range(30)}
    assert len(samples) > 1


def test_sample_decode_output_length_grows_by_num_new_tokens():
    rng = np.random.RandomState(4)
    vocab_size, d_model, num_heads, seq_len = 10, 4, 2, 3
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    embedding_table = rng.randn(vocab_size, d_model)

    result = sample_decode(
        token_ids,
        embedding_table,
        blocks_params=[],
        num_heads=num_heads,
        tied=True,
        output_weight=None,
        num_new_tokens=5,
        temperature=1.0,
        top_k=None,
        rng=rng,
    )
    assert result.shape == (1, seq_len + 5)


def test_sample_decode_preserves_the_original_prefix():
    rng = np.random.RandomState(5)
    vocab_size, d_model, num_heads, seq_len = 10, 4, 2, 3
    token_ids = rng.randint(0, vocab_size, size=(1, seq_len))
    embedding_table = rng.randn(vocab_size, d_model)

    result = sample_decode(
        token_ids,
        embedding_table,
        blocks_params=[],
        num_heads=num_heads,
        tied=True,
        output_weight=None,
        num_new_tokens=4,
        temperature=1.0,
        top_k=None,
        rng=rng,
    )
    assert np.array_equal(result[:, :seq_len], token_ids)
