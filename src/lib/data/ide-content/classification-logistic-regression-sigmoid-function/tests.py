import numpy as np


def run_tests():
    tests = []

    try:
        result = sigmoid(np.array([0.0]))
        np.testing.assert_allclose(result, [0.5], atol=1e-6)
        tests.append({"name": "test_zero_is_half", "passed": True, "error": None})
    except Exception as e:
        tests.append({"name": "test_zero_is_half", "passed": False, "error": str(e)})

    try:
        result = sigmoid(np.array([2.0, -2.0]))
        np.testing.assert_allclose(result, [0.8807971, 0.1192029], atol=1e-5)
        tests.append({"name": "test_known_values", "passed": True, "error": None})
    except Exception as e:
        tests.append({"name": "test_known_values", "passed": False, "error": str(e)})

    try:
        result = sigmoid(np.array([-50.0, 50.0]))
        assert result[0] < 1e-6, f"Expected near 0, got {result[0]}"
        assert result[1] > 1 - 1e-6, f"Expected near 1, got {result[1]}"
        tests.append({"name": "test_saturates_at_extremes", "passed": True, "error": None})
    except Exception as e:
        tests.append({"name": "test_saturates_at_extremes", "passed": False, "error": str(e)})

    return tests
