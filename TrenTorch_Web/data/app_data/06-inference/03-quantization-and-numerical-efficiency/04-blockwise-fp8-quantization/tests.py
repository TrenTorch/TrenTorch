"""
pytest data/app_data/06-inference/03-quantization-and-numerical-efficiency/04-blockwise-fp8-quantization/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

quantize_fp8_blockwise = load_solution(
    f"06-inference/03-quantization-and-numerical-efficiency/{Path(__file__).resolve().parent.name}"
).quantize_fp8_blockwise


def test_single_2x2_block_shape_and_scale():
    result = quantize_fp8_blockwise(np.array([[100.0, 1.0], [0.01, -50.0]]), block_rows=2, block_cols=2)
    assert result["scale"].shape == (1, 1)
    assert np.isclose(result["scale"][0, 0], 100.0 / 448.0)


def test_small_value_not_crushed_to_zero_unlike_int8():
    # 0.01 next to a block max of 100 keeps a nonzero simulated FP8 value
    # -- an INT8 scheme with the same block max would round it to 0.
    result = quantize_fp8_blockwise(np.array([[100.0, 1.0], [0.01, -50.0]]), block_rows=2, block_cols=2)
    assert result["dequantized"][1, 0] != 0.0
    # Relative error should still be small (FP8's whole point).
    rel_error = abs(result["dequantized"][1, 0] - 0.01) / 0.01
    assert rel_error < 0.2


def test_grid_of_1x1_blocks_each_own_scale():
    result = quantize_fp8_blockwise(np.array([[1.0, 100.0], [0.5, -2.0]]), block_rows=1, block_cols=1)
    assert result["scale"].shape == (2, 2)
    # Each 1x1 "block" is exactly its own value scaled to fill 448 -> dequant ~ original.
    assert np.allclose(result["dequantized"], [[1.0, 100.0], [0.5, -2.0]], rtol=0.15)


def test_block_containing_all_zeros():
    result = quantize_fp8_blockwise(np.array([[0.0, 0.0], [0.0, 0.0]]), block_rows=2, block_cols=2)
    assert result["scale"][0, 0] == 0.0
    assert np.array_equal(result["dequantized"], [[0.0, 0.0], [0.0, 0.0]])


def test_relative_error_stays_bounded_across_magnitudes():
    # Unlike linear (INT) quantization, FP8's relative error for values
    # spanning several orders of magnitude within one block should stay
    # roughly similar, not blow up for the smallest value.
    W = np.array([[1000.0, 100.0, 10.0, 1.0]])
    result = quantize_fp8_blockwise(W, block_rows=1, block_cols=4)
    rel_errors = np.abs(W - result["dequantized"]) / np.abs(W)
    assert np.max(rel_errors) < 0.15
