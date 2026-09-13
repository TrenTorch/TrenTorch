"""
pytest data/app_data/09-systems-distributed/01-memoization/02-benchmark-with-vs-without-cache/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"09-systems-distributed/01-memoization/{Path(__file__).resolve().parent.name}")
naive_kv_projection_work = _module.naive_kv_projection_work
cached_kv_projection_work = _module.cached_kv_projection_work
cache_work_reduction_factor = _module.cache_work_reduction_factor


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_naive_work_matches_hand_computation():
    # prompt_len=5, 3 new tokens -> lengths 6, 7, 8 -> total 21
    assert naive_kv_projection_work(5, 3) == 21


def test_02_cached_work_matches_hand_computation():
    assert cached_kv_projection_work(5, 3) == 8


# --- Shape / general-case coverage -----------------------------------


def test_03_naive_work_matches_the_closed_form_arithmetic_series():
    # sum_{i=1}^{N} (P+i) = N*P + N*(N+1)/2
    prompt_len, num_new = 10, 20
    closed_form = num_new * prompt_len + num_new * (num_new + 1) // 2
    assert naive_kv_projection_work(prompt_len, num_new) == closed_form


def test_04_cached_work_is_always_linear_in_num_new_tokens():
    for num_new in [1, 10, 100]:
        assert cached_kv_projection_work(50, num_new) == 50 + num_new


# --- Parameter handling -------------------------------------------------


def test_05_reduction_factor_grows_as_generation_gets_longer():
    # The longer the generation, the more redundant work naive
    # re-projection accumulates relative to the cache -- this IS the
    # actual, quantitative case for why KV-caching matters more and
    # more as sequences get longer.
    short_gen = cache_work_reduction_factor(prompt_len=10, num_new_tokens=5)
    long_gen = cache_work_reduction_factor(prompt_len=10, num_new_tokens=500)
    assert long_gen > short_gen


def test_06_reduction_factor_matches_ratio_of_the_two_work_functions():
    prompt_len, num_new = 20, 15
    expected = naive_kv_projection_work(prompt_len, num_new) / cached_kv_projection_work(prompt_len, num_new)
    assert cache_work_reduction_factor(prompt_len, num_new) == expected


# --- Edge cases ---------------------------------------------------------


def test_07_zero_new_tokens_needs_no_extra_work_either_way():
    assert naive_kv_projection_work(10, 0) == 0
    assert cached_kv_projection_work(10, 0) == 10
    assert cache_work_reduction_factor(10, 0) == 0.0


def test_08_single_new_token_naive_and_cached_agree():
    # For exactly one new token, both approaches project the same
    # prompt_len+1 tokens' worth of K/V -- the redundancy only appears
    # from the SECOND new token onward.
    assert naive_kv_projection_work(10, 1) == cached_kv_projection_work(10, 1)


# --- Array hygiene / determinism -----------------------------------------


def test_09_functions_are_pure():
    results = {naive_kv_projection_work(30, 12) for _ in range(5)}
    assert len(results) == 1


# --- Independent correctness oracle -----------------------------------


def test_10_matches_the_real_measured_generate_without_cache_work_pattern():
    # Cross-checks this question's analytical accounting against
    # 01-kv-cache-autoregressive-generation's actual, real implementation:
    # generate_without_cache genuinely reprojects the full sequence at
    # every step, so its per-step sequence lengths are exactly
    # prompt_len+1, prompt_len+2, ..., prompt_len+num_new_tokens --
    # precisely what naive_kv_projection_work sums.
    kv_cache_module = load_solution(
        "09-systems-distributed/01-memoization/01-kv-cache-autoregressive-generation"
    )
    import numpy as np

    rng = np.random.default_rng(0)
    prompt_len, d_model, num_new = 4, 3, 6
    X_prompt = rng.normal(size=(prompt_len, d_model))
    W_Q, W_K, W_V = (rng.normal(size=(d_model, d_model)) for _ in range(3))
    new_tokens = [rng.normal(size=d_model) for _ in range(num_new)]

    result = kv_cache_module.generate_without_cache(X_prompt, W_Q, W_K, W_V, new_tokens)
    assert result["final_cache_len"] == prompt_len + num_new  # the real sequence really does grow this way
    assert naive_kv_projection_work(prompt_len, num_new) == sum(
        prompt_len + i for i in range(1, num_new + 1)
    )
