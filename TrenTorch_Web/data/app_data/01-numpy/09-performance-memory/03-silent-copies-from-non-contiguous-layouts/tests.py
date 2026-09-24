"""
pytest data/app_data/01-numpy/09-performance-memory/03-silent-copies-from-non-contiguous-layouts/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/09-performance-memory/{Path(__file__).resolve().parent.name}")
reshape_copies = _module.reshape_copies
ravel_copies = _module.ravel_copies
ensure_contiguous = _module.ensure_contiguous
reshape_write_propagates = _module.reshape_write_propagates


def test_c_contiguous_reshape_is_a_view():
    assert reshape_copies(np.arange(12), (3, 4)) is False
    assert reshape_copies(np.arange(12).reshape(3, 4), (2, 6)) is False


def test_reshaping_transposed_array_to_1d_copies():
    t = np.arange(6).reshape(2, 3).T
    assert reshape_copies(t, (6,)) is True


def test_reshaping_transpose_to_compatible_shape_is_still_a_view():
    t = np.arange(6).reshape(2, 3).T
    assert reshape_copies(t, t.shape) is False


def test_ravel_copies_depends_on_layout():
    contiguous = np.arange(6).reshape(2, 3)
    assert ravel_copies(contiguous) is False

    transposed = contiguous.T
    assert ravel_copies(transposed) is True

    wide = np.arange(12).reshape(3, 4)
    column = wide[:, 0]
    assert ravel_copies(column) is True


def test_ensure_contiguous_fixes_non_contiguity():
    arr = np.arange(12).reshape(3, 4)
    for candidate in [arr.T, arr[:, ::2]]:
        result = ensure_contiguous(candidate)
        assert result.flags["C_CONTIGUOUS"]
        np.testing.assert_array_equal(result, candidate)


def test_ensure_contiguous_avoids_needless_copies():
    arr = np.arange(12).reshape(3, 4)
    result = ensure_contiguous(arr)
    assert np.shares_memory(arr, result)


def test_write_through_depends_on_view_vs_copy():
    contiguous = np.arange(12).reshape(3, 4)
    assert reshape_write_propagates(contiguous, (2, 6), 99) is True

    t = np.arange(6).reshape(2, 3).T.copy().T
    original = t.copy()
    result = reshape_write_propagates(t, (6,), 99)
    assert result is False
    np.testing.assert_array_equal(t, original)
