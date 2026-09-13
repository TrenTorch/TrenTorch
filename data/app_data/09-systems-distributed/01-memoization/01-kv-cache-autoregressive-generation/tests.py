"""
pytest data/app_data/09-systems-distributed/01-memoization/01-kv-cache-autoregressive-generation/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"09-systems-distributed/01-memoization/{Path(__file__).resolve().parent.name}")
generate_without_cache = _module.generate_without_cache
outputs_match = _module.outputs_match
autoregressive_decode_with_cache = load_solution(
    "06-inference/02-kv-cache-and-decoding/02-autoregressive-decoding-kv-cache"
).autoregressive_decode_with_cache


def _random_setup(seed, prompt_len=3, d_model=4, num_new=3):
    rng = np.random.default_rng(seed)
    X_prompt = rng.normal(size=(prompt_len, d_model))
    W_Q = rng.normal(size=(d_model, d_model))
    W_K = rng.normal(size=(d_model, d_model))
    W_V = rng.normal(size=(d_model, d_model))
    new_tokens = [rng.normal(size=d_model) for _ in range(num_new)]
    return X_prompt, W_Q, W_K, W_V, new_tokens


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_output_shapes_match_the_cached_versions():
    X_prompt, W_Q, W_K, W_V, new_tokens = _random_setup(0)
    result = generate_without_cache(X_prompt, W_Q, W_K, W_V, new_tokens)
    assert result["prefill_output"].shape == X_prompt.shape
    assert result["generated_outputs"].shape == (len(new_tokens), X_prompt.shape[1])


def test_02_outputs_match_matches_two_genuinely_identical_implementations():
    X_prompt, W_Q, W_K, W_V, new_tokens = _random_setup(1)
    assert outputs_match(X_prompt, W_Q, W_K, W_V, new_tokens) is True


# --- Shape / general-case coverage -----------------------------------


def test_03_prefill_output_matches_the_cached_implementation_exactly():
    X_prompt, W_Q, W_K, W_V, new_tokens = _random_setup(2)
    cached = autoregressive_decode_with_cache(X_prompt, W_Q, W_K, W_V, new_tokens)
    uncached = generate_without_cache(X_prompt, W_Q, W_K, W_V, new_tokens)
    assert np.allclose(cached["prefill_output"], uncached["prefill_output"], atol=1e-8)


def test_04_every_generated_step_matches_the_cached_implementation_exactly():
    X_prompt, W_Q, W_K, W_V, new_tokens = _random_setup(3, num_new=5)
    cached = autoregressive_decode_with_cache(X_prompt, W_Q, W_K, W_V, new_tokens)
    uncached = generate_without_cache(X_prompt, W_Q, W_K, W_V, new_tokens)
    assert np.allclose(cached["generated_outputs"], uncached["generated_outputs"], atol=1e-8)


# --- Parameter handling -------------------------------------------------


def test_05_final_cache_len_accounts_for_every_new_token():
    X_prompt, W_Q, W_K, W_V, new_tokens = _random_setup(4, prompt_len=2, num_new=4)
    result = generate_without_cache(X_prompt, W_Q, W_K, W_V, new_tokens)
    assert result["final_cache_len"] == 2 + 4


def test_06_works_with_different_prompt_lengths():
    for prompt_len in [1, 5, 10]:
        X_prompt, W_Q, W_K, W_V, new_tokens = _random_setup(5, prompt_len=prompt_len, num_new=2)
        result = generate_without_cache(X_prompt, W_Q, W_K, W_V, new_tokens)
        assert result["final_cache_len"] == prompt_len + 2


# --- Edge cases ---------------------------------------------------------


def test_07_no_new_tokens_returns_only_the_prefill_output():
    X_prompt, W_Q, W_K, W_V, _ = _random_setup(6, num_new=0)
    result = generate_without_cache(X_prompt, W_Q, W_K, W_V, [])
    assert result["generated_outputs"].shape == (0, X_prompt.shape[1])
    assert result["final_cache_len"] == X_prompt.shape[0]


def test_08_single_token_prompt_works():
    X_prompt, W_Q, W_K, W_V, new_tokens = _random_setup(7, prompt_len=1, num_new=2)
    result = generate_without_cache(X_prompt, W_Q, W_K, W_V, new_tokens)
    assert result["prefill_output"].shape == (1, X_prompt.shape[1])


# --- Array hygiene ------------------------------------------------------


def test_09_does_not_mutate_its_inputs():
    X_prompt, W_Q, W_K, W_V, new_tokens = _random_setup(8)
    X_prompt_copy = X_prompt.copy()
    W_Q_copy, W_K_copy, W_V_copy = W_Q.copy(), W_K.copy(), W_V.copy()
    generate_without_cache(X_prompt, W_Q, W_K, W_V, new_tokens)
    assert np.array_equal(X_prompt, X_prompt_copy)
    assert np.array_equal(W_Q, W_Q_copy)
    assert np.array_equal(W_K, W_K_copy)
    assert np.array_equal(W_V, W_V_copy)


# --- Independent correctness oracle -----------------------------------


def test_10_outputs_match_correctly_detects_a_genuine_mismatch():
    # A sanity check on outputs_match itself: it must not be a function
    # that always returns True regardless of input -- feeding it
    # deliberately DIFFERENT weight matrices for the two calls should
    # make it correctly report False.
    X_prompt, W_Q, W_K, W_V, new_tokens = _random_setup(9)
    cached = autoregressive_decode_with_cache(X_prompt, W_Q, W_K, W_V, new_tokens)
    wrong_W_V = W_V + 5.0  # deliberately different
    uncached_wrong = generate_without_cache(X_prompt, W_Q, W_K, wrong_W_V, new_tokens)
    assert not np.allclose(cached["generated_outputs"], uncached_wrong["generated_outputs"])
    assert outputs_match(X_prompt, W_Q, W_K, W_V, new_tokens) is True
