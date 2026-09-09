import numpy as np


def run_tests():
    tests = []

    # Test 1: Tensor Creation & Attributes
    try:
        t = Tensor([[1, 2, 3], [4, 5, 6]])
        assert t.shape == (2, 3), f"Expected shape (2,3), got {t.shape}"
        assert t.ndim == 2, f"Expected ndim 2, got {t.ndim}"
        assert t.size == 6, f"Expected size 6, got {t.size}"
        assert t.data.dtype == np.float32, "Expected dtype float32"
        tests.append({"name": "test_tensor_creation", "passed": True, "error": None})
    except Exception as e:
        tests.append({"name": "test_tensor_creation", "passed": False, "error": str(e)})

    # Test 2: Arithmetic Operations (Add, Sub, Mul)
    try:
        a = Tensor([1.0, 2.0, 3.0])
        b = Tensor([4.0, 5.0, 6.0])
        add_res = (a + b).data
        np.testing.assert_allclose(add_res, [5.0, 7.0, 9.0], err_msg="Addition failed")

        sub_res = (b - a).data
        np.testing.assert_allclose(sub_res, [3.0, 3.0, 3.0], err_msg="Subtraction failed")

        mul_res = (a * 2.0).data
        np.testing.assert_allclose(mul_res, [2.0, 4.0, 6.0], err_msg="Scalar multiplication failed")
        tests.append({"name": "test_arithmetic_operations", "passed": True, "error": None})
    except Exception as e:
        tests.append({"name": "test_arithmetic_operations", "passed": False, "error": str(e)})

    # Test 3: Matrix Multiplication
    try:
        x = Tensor([[1.0, 2.0], [3.0, 4.0]])
        y = Tensor([[2.0, 0.0], [1.0, 2.0]])
        mm = (x @ y).data
        expected = np.array([[4.0, 4.0], [10.0, 8.0]])
        np.testing.assert_allclose(mm, expected, err_msg="Matmul failed")
        tests.append({"name": "test_matrix_multiplication", "passed": True, "error": None})
    except Exception as e:
        tests.append({"name": "test_matrix_multiplication", "passed": False, "error": str(e)})

    # Test 4: Reshape & Transpose
    try:
        m = Tensor([[1, 2, 3], [4, 5, 6]])
        r = m.reshape(3, 2)
        assert r.shape == (3, 2), f"Expected shape (3,2), got {r.shape}"

        tr = m.transpose()
        assert tr.shape == (3, 2), f"Expected shape (3,2), got {tr.shape}"
        np.testing.assert_allclose(tr.data[0], [1.0, 4.0], err_msg="Transpose values mismatch")
        tests.append({"name": "test_reshape_and_transpose", "passed": True, "error": None})
    except Exception as e:
        tests.append({"name": "test_reshape_and_transpose", "passed": False, "error": str(e)})

    # Test 5: Sum Reduction
    try:
        s = Tensor([[1.0, 2.0], [3.0, 4.0]])
        assert float(s.sum().data) == 10.0, "Sum total mismatch"
        axis_sum = s.sum(axis=0).data
        np.testing.assert_allclose(axis_sum, [4.0, 6.0], err_msg="Axis sum mismatch")
        tests.append({"name": "test_sum_reduction", "passed": True, "error": None})
    except Exception as e:
        tests.append({"name": "test_sum_reduction", "passed": False, "error": str(e)})

    return tests
