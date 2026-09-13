"""
pytest data/app_data/08-systems-performance/03-mixed-precision-training/03-autocast-concept/tests.py
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"08-systems-performance/03-mixed-precision-training/{Path(__file__).resolve().parent.name}")
should_run_in_fp16 = _module.should_run_in_fp16
autocast_dtype_for = _module.autocast_dtype_for


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_matmul_is_fp16_safe():
    assert should_run_in_fp16("matmul") is True


def test_02_softmax_requires_fp32():
    assert should_run_in_fp16("softmax") is False


# --- Shape / general-case coverage -----------------------------------


def test_03_every_matmul_like_op_is_fp16_safe():
    for op in ["matmul", "linear", "conv2d", "relu"]:
        assert should_run_in_fp16(op) is True


def test_04_every_reduction_or_normalization_op_requires_fp32():
    for op in ["softmax", "log_softmax", "layer_norm", "batch_norm", "cross_entropy", "sum", "mean"]:
        assert should_run_in_fp16(op) is False


# --- Parameter handling -------------------------------------------------


def test_05_autocast_dtype_for_matches_should_run_in_fp16():
    assert autocast_dtype_for("matmul") == "float16"
    assert autocast_dtype_for("softmax") == "float32"


def test_06_unknown_op_raises_value_error():
    with pytest.raises(ValueError):
        should_run_in_fp16("some_made_up_op")


def test_07_unknown_op_raises_from_autocast_dtype_for_too():
    with pytest.raises(ValueError):
        autocast_dtype_for("some_made_up_op")


# --- Edge cases ---------------------------------------------------------


def test_08_exp_and_log_both_require_fp32():
    # exponentials and logarithms amplify small errors dramatically,
    # exactly why softmax (which uses both internally) needs fp32.
    assert should_run_in_fp16("exp") is False
    assert should_run_in_fp16("log") is False


def test_09_no_op_name_is_in_both_lists_at_once():
    fp16_safe = {"matmul", "linear", "conv2d", "relu"}
    fp32_required = {
        "softmax",
        "log_softmax",
        "layer_norm",
        "batch_norm",
        "cross_entropy",
        "sum",
        "mean",
        "exp",
        "log",
    }
    assert fp16_safe.isdisjoint(fp32_required)
    for op in fp16_safe:
        assert should_run_in_fp16(op) is True
    for op in fp32_required:
        assert should_run_in_fp16(op) is False


# --- Array hygiene / determinism -----------------------------------------


def test_10_the_same_op_always_gets_the_same_answer():
    results = [should_run_in_fp16("matmul") for _ in range(5)]
    assert all(r is True for r in results)


# --- Independent correctness oracle -----------------------------------


def test_11_matches_pytorchs_own_documented_autocast_op_categories():
    # Ground truth from PyTorch's own documentation (torch.autocast /
    # torch.cuda.amp op reference lists), not our own derivation:
    # matmul-family ops (matmul, addmm/linear, conv2d) are listed under
    # "Ops that autocast to float16"; reduction and normalization ops
    # (softmax, layer_norm, batch_norm, cross_entropy/nll_loss, sum) are
    # listed under "Ops that autocast to float32" specifically because
    # they're numerically sensitive to reduced precision. This exercise's
    # two op lists mirror those real, published categories.
    #
    # This test needs no torch installed to run.
    assert should_run_in_fp16("conv2d") is True
    assert should_run_in_fp16("linear") is True
    assert should_run_in_fp16("layer_norm") is False
    assert should_run_in_fp16("batch_norm") is False
    assert should_run_in_fp16("cross_entropy") is False
