"""
pytest data/app_data/05-transformers-llm/02-modern-transformer-architecture/03-attention-quadratic-complexity/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"05-transformers-llm/02-modern-transformer-architecture/{Path(__file__).resolve().parent.name}"
)
attention_compute_cost = _module.attention_compute_cost
attention_memory_elements = _module.attention_memory_elements
ffn_compute_cost = _module.ffn_compute_cost


def test_doubling_seq_len_roughly_quadruples_attention_compute_cost():
    d_model = 512
    cost_512 = attention_compute_cost(512, d_model)
    cost_1024 = attention_compute_cost(1024, d_model)
    ratio = cost_1024 / cost_512
    assert abs(ratio - 4.0) < 1e-6


def test_doubling_seq_len_only_doubles_ffn_compute_cost():
    d_model, d_ff = 512, 2048
    cost_512 = ffn_compute_cost(512, d_model, d_ff)
    cost_1024 = ffn_compute_cost(1024, d_model, d_ff)
    ratio = cost_1024 / cost_512
    assert abs(ratio - 2.0) < 1e-6


def test_doubling_seq_len_quadruples_attention_memory_elements():
    num_heads = 8
    mem_512 = attention_memory_elements(512, num_heads)
    mem_1024 = attention_memory_elements(1024, num_heads)
    ratio = mem_1024 / mem_512
    assert abs(ratio - 4.0) < 1e-6


def test_attention_cost_scales_linearly_in_d_model_not_quadratically():
    seq_len = 256
    cost_256 = attention_compute_cost(seq_len, 256)
    cost_512 = attention_compute_cost(seq_len, 512)
    ratio = cost_512 / cost_256
    assert abs(ratio - 2.0) < 1e-6


def test_at_long_enough_context_attention_cost_dominates_ffn_cost():
    # A concrete illustration of why "context length is expensive": for a
    # fixed model size, attention's cost grows quadratically with
    # sequence length while the FFN's stays linear, so past some crossover
    # point, attention becomes the dominant cost, even though at typical
    # (much shorter) training sequence lengths the FFN usually dominates.
    d_model, d_ff, num_heads = 4096, 4 * 4096, 32

    short_seq_len = 512
    long_seq_len = 131072  # a long-context regime

    short_attn = attention_compute_cost(short_seq_len, d_model)
    short_ffn = ffn_compute_cost(short_seq_len, d_model, d_ff)
    assert short_attn < short_ffn  # FFN dominates at typical training lengths

    long_attn = attention_compute_cost(long_seq_len, d_model)
    long_ffn = ffn_compute_cost(long_seq_len, d_model, d_ff)
    assert long_attn > long_ffn  # attention dominates at long context


def test_attention_compute_cost_uses_seq_len_squared_not_seq_len():
    # Directly targets a mutant that computes a LINEAR cost in seq_len
    # (e.g. forgetting one factor of seq_len), which would hide the
    # quadratic scaling entirely.
    d_model = 64
    cost_10 = attention_compute_cost(10, d_model)
    cost_100 = attention_compute_cost(100, d_model)
    ratio = cost_100 / cost_10
    assert abs(ratio - 100.0) < 1e-6  # 10x seq_len -> 100x cost, not 10x
