"""
pytest data/app_data/01-numpy/10-bridging-to-tensors/03-gradient-tracking/tests.py
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/10-bridging-to-tensors/{Path(__file__).resolve().parent.name}")
make_tensor_record = _module.make_tensor_record
add_records = _module.add_records
detach_record = _module.detach_record
to_device_record = _module.to_device_record


def test_record_construction():
    data = np.array([1.0, 2.0, 3.0])
    rec = make_tensor_record(data)
    assert np.shares_memory(rec["data"], data)
    assert rec["device"] == "cpu"
    assert rec["requires_grad"] is False

    rec2 = make_tensor_record(data, device="cuda", requires_grad=True)
    assert rec2["device"] == "cuda"
    assert rec2["requires_grad"] is True


def test_result_data_and_broadcasting():
    a = make_tensor_record(np.ones((3, 4)))
    b = make_tensor_record(np.array([1.0, 2.0, 3.0, 4.0]))
    result = add_records(a, b)
    np.testing.assert_array_equal(result["data"], a["data"] + b["data"])


def test_requires_grad_propagation():
    a = make_tensor_record(np.zeros(3), requires_grad=True)
    b = make_tensor_record(np.zeros(3), requires_grad=False)
    assert add_records(a, b)["requires_grad"] is True
    assert add_records(b, a)["requires_grad"] is True
    assert add_records(a, a)["requires_grad"] is True
    assert add_records(b, b)["requires_grad"] is False


def test_device_mismatch_raises():
    a = make_tensor_record(np.zeros(3), device="cpu")
    b = make_tensor_record(np.zeros(3), device="cuda")
    with pytest.raises(ValueError):
        add_records(a, b)

    c = make_tensor_record(np.zeros(3), device="cuda")
    result = add_records(b, c)
    assert result["device"] == "cuda"


def test_operands_not_mutated():
    a = make_tensor_record(np.array([1.0, 2.0]), requires_grad=True)
    b = make_tensor_record(np.array([3.0, 4.0]), requires_grad=False)
    a_data_before = a["data"].copy()
    add_records(a, b)
    np.testing.assert_array_equal(a["data"], a_data_before)
    assert a["requires_grad"] is True
    assert b["requires_grad"] is False


def test_detach_record_shares_the_buffer():
    original = make_tensor_record(np.array([1.0, 2.0, 3.0]), requires_grad=True)
    detached = detach_record(original)
    assert detached["requires_grad"] is False
    assert np.shares_memory(detached["data"], original["data"])
    detached["data"][0] = 99.0
    assert original["data"][0] == 99.0


def test_to_device_record_same_device_returns_same_object():
    rec = make_tensor_record(np.zeros(3), device="cpu")
    assert to_device_record(rec, "cpu") is rec


def test_to_device_record_different_device_copies():
    rec = make_tensor_record(np.array([1.0, 2.0]), device="cpu", requires_grad=True)
    moved = to_device_record(rec, "cuda")
    assert moved["device"] == "cuda"
    np.testing.assert_array_equal(moved["data"], rec["data"])
    assert not np.shares_memory(moved["data"], rec["data"])
    assert moved["requires_grad"] is True
    moved["data"][0] = 99.0
    assert rec["data"][0] == 1.0
