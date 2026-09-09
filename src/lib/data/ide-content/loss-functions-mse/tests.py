import numpy as np


def run_tests():
    tests = []

    try:
        result = mse_loss(np.array([1.0, 2.0, 3.0]), np.array([1.0, 2.0, 3.0]))
        np.testing.assert_allclose(float(result), 0.0)
        tests.append({"name": "test_perfect_prediction_is_zero", "passed": True, "error": None})
    except Exception as e:
        tests.append({"name": "test_perfect_prediction_is_zero", "passed": False, "error": str(e)})

    try:
        result = mse_loss(np.array([1.0, 2.0, 3.0]), np.array([1.0, 2.0, 5.0]))
        np.testing.assert_allclose(float(result), 4.0 / 3.0, atol=1e-6)
        tests.append({"name": "test_known_value", "passed": True, "error": None})
    except Exception as e:
        tests.append({"name": "test_known_value", "passed": False, "error": str(e)})

    try:
        y_pred = np.array([0.0, 0.0])
        y_true = np.array([2.0, -2.0])
        result = mse_loss(y_pred, y_true)
        np.testing.assert_allclose(float(result), 4.0)
        tests.append({"name": "test_symmetric_error", "passed": True, "error": None})
    except Exception as e:
        tests.append({"name": "test_symmetric_error", "passed": False, "error": str(e)})

    return tests
