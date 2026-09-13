"""
pytest data/app_data/08-systems-performance/01-profiling/04-flops-estimation/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"08-systems-performance/01-profiling/{Path(__file__).resolve().parent.name}")
linear_flops = _module.linear_flops
conv2d_flops = _module.conv2d_flops


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_linear_flops_no_bias_matches_hand_computation():
    # batch=1, in=10, out=4: multiply_adds = 40, flops = 80
    assert linear_flops(1, 10, 4, bias=False) == 80


def test_02_conv2d_flops_no_bias_matches_hand_computation():
    # batch=1, in_c=3, out_c=8, kernel=3, output 5x5:
    # output_positions = 1*8*5*5 = 200
    # multiply_adds_per_position = 3*3*3 = 27
    # flops = 2 * 200 * 27 = 10800
    assert conv2d_flops(1, 3, 8, 3, 5, 5, bias=False) == 10800


# --- Shape / general-case coverage -----------------------------------


def test_03_linear_flops_scales_linearly_with_batch_size():
    single = linear_flops(1, 10, 4, bias=False)
    batched = linear_flops(8, 10, 4, bias=False)
    assert batched == single * 8


def test_04_conv2d_flops_scales_with_output_spatial_size():
    small = conv2d_flops(1, 3, 8, 3, 4, 4, bias=False)
    large = conv2d_flops(1, 3, 8, 3, 8, 8, bias=False)
    assert large == small * 4  # 4x the output positions (2x height, 2x width)


# --- Parameter handling -------------------------------------------------


def test_05_linear_bias_adds_exactly_batch_times_out_features():
    no_bias = linear_flops(2, 10, 4, bias=False)
    with_bias = linear_flops(2, 10, 4, bias=True)
    assert with_bias - no_bias == 2 * 4


def test_06_conv2d_bias_adds_exactly_one_flop_per_output_position():
    no_bias = conv2d_flops(1, 3, 8, 3, 5, 5, bias=False)
    with_bias = conv2d_flops(1, 3, 8, 3, 5, 5, bias=True)
    assert with_bias - no_bias == 1 * 8 * 5 * 5


def test_07_bias_defaults_to_true():
    assert linear_flops(1, 10, 4) == linear_flops(1, 10, 4, bias=True)
    assert conv2d_flops(1, 3, 8, 3, 5, 5) == conv2d_flops(1, 3, 8, 3, 5, 5, bias=True)


# --- Edge cases ---------------------------------------------------------


def test_08_single_output_feature_or_channel_still_computes_correctly():
    assert linear_flops(1, 10, 1, bias=False) == 20
    assert conv2d_flops(1, 3, 1, 3, 1, 1, bias=False) == 2 * 1 * 27


def test_09_kernel_size_one_reduces_to_a_pointwise_conv_flop_count():
    # a 1x1 conv's per-position work is exactly in_channels multiply-adds,
    # same as a Linear layer applied per pixel.
    result = conv2d_flops(1, 3, 8, 1, 4, 4, bias=False)
    expected = 2 * (1 * 8 * 4 * 4) * (3 * 1 * 1)
    assert result == expected


# --- Independent correctness oracle -----------------------------------


def test_10_matches_the_standard_2x_macs_flop_counting_convention():
    # This is a well-established engineering convention (used by
    # profiling tools like fvcore's FlopCountAnalysis and thop), not a
    # single deep-learning-framework internal computation: a
    # multiply-accumulate (MAC) is counted as 2 FLOPs (one multiply, one
    # add). For a Linear(in_features=512, out_features=512) layer run
    # on a batch of 32:
    #   MACs = 32 * 512 * 512 = 8,388,608
    #   FLOPs (no bias) = 2 * MACs = 16,777,216
    assert linear_flops(32, 512, 512, bias=False) == 16_777_216
