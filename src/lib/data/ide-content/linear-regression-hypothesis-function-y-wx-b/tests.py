import numpy as np


def run_tests():
    tests = []

    try:
        result = predict(np.array([1.0, 2.0, 3.0]), w=2.0, b=1.0)
        np.testing.assert_allclose(result, [3.0, 5.0, 7.0])
        tests.append({"name": "test_basic_line", "passed": True, "error": None})
    except Exception as e:
        tests.append({"name": "test_basic_line", "passed": False, "error": str(e)})

    try:
        result = predict(np.array([0.0, 0.0, 0.0]), w=5.0, b=-3.0)
        np.testing.assert_allclose(result, [-3.0, -3.0, -3.0])
        tests.append({"name": "test_zero_input", "passed": True, "error": None})
    except Exception as e:
        tests.append({"name": "test_zero_input", "passed": False, "error": str(e)})

    try:
        x = np.array([[1.0, 2.0], [3.0, 4.0]])
        result = predict(x, w=0.5, b=1.0)
        np.testing.assert_allclose(result, [[1.5, 2.0], [2.5, 3.0]])
        tests.append({"name": "test_2d_shape_preserved", "passed": True, "error": None})
    except Exception as e:
        tests.append({"name": "test_2d_shape_preserved", "passed": False, "error": str(e)})

    return tests
