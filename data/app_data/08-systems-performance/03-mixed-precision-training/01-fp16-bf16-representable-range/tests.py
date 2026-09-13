"""
pytest data/app_data/08-systems-performance/03-mixed-precision-training/01-fp16-bf16-representable-range/tests.py
"""

import sys
import warnings
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"08-systems-performance/03-mixed-precision-training/{Path(__file__).resolve().parent.name}")
cast_to_dtype = _module.cast_to_dtype
detect_underflow = _module.detect_underflow
detect_overflow = _module.detect_overflow


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_a_tiny_value_underflows_to_zero_in_fp16():
    x = np.array([1e-8], dtype=np.float32)
    casted = cast_to_dtype(x, "float16")
    assert casted[0] == 0.0


def test_02_an_ordinary_value_survives_the_cast_unchanged_in_spirit():
    x = np.array([1.5], dtype=np.float32)
    casted = cast_to_dtype(x, "float16")
    assert np.isclose(casted[0], 1.5)


# --- Shape / general-case coverage -----------------------------------


def test_03_detect_underflow_flags_only_the_lost_values():
    original = np.array([1e-8, 1.0, 1e-9, 2.0], dtype=np.float32)
    casted = cast_to_dtype(original, "float16")
    mask = detect_underflow(original, casted)
    assert list(mask) == [True, False, True, False]


def test_04_zero_input_is_never_flagged_as_underflow():
    # zero casting to zero is not "underflow" -- nothing was lost.
    original = np.array([0.0, 1e-8], dtype=np.float32)
    casted = cast_to_dtype(original, "float16")
    mask = detect_underflow(original, casted)
    assert list(mask) == [False, True]


# --- Parameter handling -------------------------------------------------


def test_05_large_finite_value_overflows_fp16_to_inf():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        x = np.array([70000.0], dtype=np.float32)
        casted = cast_to_dtype(x, "float16")
    assert detect_overflow(casted)[0] == True  # noqa: E712


def test_06_a_value_at_fp16s_actual_max_does_not_overflow():
    x = np.array([65504.0], dtype=np.float32)  # fp16's real representable max
    casted = cast_to_dtype(x, "float16")
    assert not detect_overflow(casted)[0]


# --- Edge cases ---------------------------------------------------------


def test_07_negative_tiny_values_underflow_the_same_way():
    original = np.array([-1e-8], dtype=np.float32)
    casted = cast_to_dtype(original, "float16")
    assert casted[0] == 0.0
    assert detect_underflow(original, casted)[0]


def test_08_float32_to_float32_cast_never_underflows_or_overflows():
    original = np.array([1e-8, 70000.0], dtype=np.float32)
    casted = cast_to_dtype(original, "float32")
    assert not np.any(detect_underflow(original, casted))
    assert not np.any(detect_overflow(casted))


# --- Array hygiene ------------------------------------------------------


def test_09_does_not_mutate_its_input():
    original = np.array([1.0, 2.0], dtype=np.float32)
    original_copy = original.copy()
    cast_to_dtype(original, "float16")
    assert np.array_equal(original, original_copy)


# --- Independent correctness oracle -----------------------------------


def test_10_matches_real_numpy_and_torch_fp16_finfo_boundaries():
    # Ground truth from the actual libraries, not our own derivation.
    #
    # Generated once, offline, with:
    #   np.finfo(np.float16).tiny               # 6.104e-05, smallest NORMAL fp16
    #   np.finfo(np.float16).smallest_subnormal  # 6e-08, smallest representable at all
    #   np.finfo(np.float16).max                 # 65504.0
    #   torch.finfo(torch.float16) reports the identical min/max/tiny values --
    #   NumPy's float16 and PyTorch's float16 are the same IEEE-754 binary16 format.
    #
    # This test needs no torch installed to run.
    assert np.isclose(np.finfo(np.float16).tiny, 6.104e-05, atol=1e-8)
    assert np.isclose(np.finfo(np.float16).smallest_subnormal, 6e-08, atol=1e-9)
    assert np.isclose(np.finfo(np.float16).max, 65504.0)

    # A value well below half the smallest subnormal genuinely vanishes
    # (rounds to zero rather than up to the smallest representable value).
    x = np.array([1e-8], dtype=np.float32)
    casted = cast_to_dtype(x, "float16")
    assert casted[0] == 0.0
