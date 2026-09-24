"""
pytest data/app_data/01-numpy/01-array-fundamentals/07-assemble-build-and-describe/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/01-array-fundamentals/{Path(__file__).resolve().parent.name}")
build_and_describe = _module.build_and_describe


def test_correct_dispatch_across_all_four_kind_values():
    from_list = build_and_describe({"kind": "from_list", "values": [1, 2, 3], "dtype": None})
    np.testing.assert_array_equal(from_list["array"], [1, 2, 3])

    zeros = build_and_describe({"kind": "zeros", "shape": (2, 3), "dtype": None})
    assert np.all(zeros["array"] == 0)

    arange = build_and_describe({"kind": "arange", "start": 0, "stop": 10, "step": 2, "dtype": None})
    np.testing.assert_array_equal(arange["array"], [0, 2, 4, 6, 8])

    linspace = build_and_describe({"kind": "linspace", "start": 0, "stop": 10, "num": 5, "dtype": None})
    np.testing.assert_allclose(linspace["array"], [0.0, 2.5, 5.0, 7.5, 10.0])


def test_dtype_applied_correctly_when_specified():
    result = build_and_describe({"kind": "from_list", "values": [1, 2, 3], "dtype": np.float32})
    assert result["dtype"] == "float32"


def test_dtype_left_to_default_inference_when_none():
    result = build_and_describe({"kind": "from_list", "values": [1, 2, 3], "dtype": None})
    assert result["dtype"] == "int64"


def test_metadata_fields_consistent_with_built_array_1d_and_2d():
    one_d = build_and_describe({"kind": "arange", "start": 0, "stop": 5, "step": 1, "dtype": None})
    assert one_d["shape"] == one_d["array"].shape
    assert one_d["ndim"] == one_d["array"].ndim
    assert one_d["size"] == one_d["array"].size
    assert one_d["dtype"] == str(one_d["array"].dtype)

    two_d = build_and_describe({"kind": "zeros", "shape": (2, 3), "dtype": None})
    assert two_d["shape"] == (2, 3)
    assert two_d["ndim"] == 2
    assert two_d["size"] == 6


def test_multi_dimensional_zeros_spec():
    result = build_and_describe({"kind": "zeros", "shape": (3, 2), "dtype": None})
    assert result["shape"] == (3, 2)
    assert np.all(result["array"] == 0)
