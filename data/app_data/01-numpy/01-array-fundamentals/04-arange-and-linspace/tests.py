"""
pytest data/app_data/01-numpy/01-array-fundamentals/04-arange-and-linspace/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/01-array-fundamentals/{Path(__file__).resolve().parent.name}")
make_range = _module.make_range
make_evenly_spaced = _module.make_evenly_spaced
compare_arange_linspace = _module.compare_arange_linspace


def test_make_range_correct_sequence_and_exclusive_stop():
    result = make_range(0, 10, 2)
    np.testing.assert_array_equal(result, [0, 2, 4, 6, 8])
    assert 10 not in result


def test_make_evenly_spaced_correct_count_and_inclusive_endpoints():
    result = make_evenly_spaced(0, 10, 5)
    assert len(result) == 5
    assert result[0] == 0
    assert result[-1] == 10


def test_non_integer_step_handling():
    result = make_range(0, 1, 0.25)
    np.testing.assert_allclose(result, [0.0, 0.25, 0.5, 0.75])


def test_compare_arange_linspace_correctly_reports_endpoint_inclusion():
    result = compare_arange_linspace(0, 10, 2)
    assert result["arange_includes_stop"] is False
    assert result["linspace_includes_stop"] is True
