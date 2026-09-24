"""
pytest data/app_data/01-numpy/03-views-vs-copies/06-assemble-trace-ownership/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/03-views-vs-copies/{Path(__file__).resolve().parent.name}")
trace_pipeline = _module.trace_pipeline


def test_correct_values_at_each_step_before_mutation():
    arr = np.arange(10, 20)
    result = trace_pipeline(arr)
    np.testing.assert_array_equal(result["step_b"], [12, 14, 16])
    np.testing.assert_array_equal(result["step_c"][:3], [12, 13, 14])


def test_correct_memory_sharing_classification():
    arr = np.arange(10, 20)
    result = trace_pipeline(arr)
    assert result["step_a_shares_memory_with_arr"] is True
    assert result["step_b_shares_memory_with_arr"] is False
    assert result["step_c_shares_memory_with_arr"] is False


def test_correct_ultimate_owner_tracing():
    arr = np.arange(10, 20)
    result = trace_pipeline(arr)
    assert result["step_a_ultimate_owner_is_arr"] is True


def test_mutation_propagates_only_to_genuinely_shared_buffers():
    arr = np.arange(10, 20)
    result = trace_pipeline(arr)
    assert result["arr_reflects_mutation"] is True
    assert result["step_b_reflects_mutation"] is False
    assert result["step_c_reflects_mutation"] is False


def test_position_correctness_of_propagated_mutation():
    arr = np.arange(10, 20)
    result = trace_pipeline(arr)
    assert arr[2] == -1
    assert result["arr_after_mutation"][2] == -1
