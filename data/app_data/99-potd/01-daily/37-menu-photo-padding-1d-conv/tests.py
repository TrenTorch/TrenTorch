"""
pytest data/app_data/99-potd/01-daily/37-menu-photo-padding-1d-conv/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
conv1d = _module.conv1d


def test_example_valid_mode_matches_the_specs_worked_values():
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    kernel = np.array([1.0, 0.0, -1.0])
    result = conv1d(x, kernel, "valid")
    np.testing.assert_allclose(result, [-2.0, -2.0, -2.0], atol=1e-6)


def test_example_same_mode_matches_the_specs_worked_values():
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    kernel = np.array([1.0, 0.0, -1.0])
    result = conv1d(x, kernel, "same")
    np.testing.assert_allclose(result, [-2.0, -2.0, -2.0, -2.0, 4.0], atol=1e-6)
    assert len(result) == len(x)


def test_valid_output_length_is_n_minus_k_plus_one():
    x = np.arange(10, dtype=float)
    kernel = np.ones(5)
    result = conv1d(x, kernel, "valid")
    assert len(result) == 10 - 5 + 1


def test_kernel_size_one_gives_identical_valid_and_same_output():
    x = np.array([2.0, -3.0, 5.0, 7.0])
    kernel = np.array([4.0])
    valid = conv1d(x, kernel, "valid")
    same = conv1d(x, kernel, "same")
    np.testing.assert_allclose(valid, same, atol=1e-9)
    np.testing.assert_allclose(valid, x * 4.0, atol=1e-9)


def test_kernel_is_not_flipped_cross_correlation_not_true_convolution():
    x = np.array([1.0, 0.0, 0.0, 0.0, 0.0])
    kernel = np.array([1.0, 2.0, 3.0])
    result = conv1d(x, kernel, "valid")
    # window [1,0,0] . [1,2,3] = 1, not the flipped-kernel answer (which
    # would put the 3 first and give a different leading value).
    assert abs(result[0] - 1.0) < 1e-9


def test_same_mode_boundary_is_zero_not_wrapped_or_clamped():
    x = np.array([5.0, 0.0, 0.0, 0.0, 0.0])
    kernel = np.array([1.0, 1.0, 1.0])
    result = conv1d(x, kernel, "same")
    # position 0's window is [pad=0, x0=5, x1=0] -> sum = 5, not wrapped to
    # the far end of x and not clamped to repeat x0.
    assert abs(result[0] - 5.0) < 1e-9


def test_matches_a_reference_on_random_signals():
    rng = np.random.default_rng(33)
    for _ in range(15):
        n = int(rng.integers(3, 50))
        k = int(rng.choice([1, 3, 5, 7]))
        if k > n:
            continue
        x = rng.uniform(-5, 5, size=n)
        kernel = rng.uniform(-2, 2, size=k)
        for mode in ["valid", "same"]:
            if mode == "same":
                pad = k // 2
                padded = np.concatenate([np.zeros(pad), x, np.zeros(pad)])
            else:
                padded = x
            expected_len = len(padded) - k + 1
            expected = np.array([np.sum(padded[i : i + k] * kernel) for i in range(expected_len)])
            np.testing.assert_allclose(conv1d(x, kernel, mode), expected, atol=1e-6)
