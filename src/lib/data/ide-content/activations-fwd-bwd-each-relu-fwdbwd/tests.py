import numpy as np


def run_tests():
    tests = []

    try:
        result = relu_forward(np.array([-2.0, -0.5, 0.0, 0.5, 2.0]))
        np.testing.assert_allclose(result, [0.0, 0.0, 0.0, 0.5, 2.0])
        tests.append({"name": "test_forward_clips_negatives", "passed": True, "error": None})
    except Exception as e:
        tests.append({"name": "test_forward_clips_negatives", "passed": False, "error": str(e)})

    try:
        x = np.array([[-1.0, 2.0], [3.0, -4.0]])
        result = relu_forward(x)
        np.testing.assert_allclose(result, [[0.0, 2.0], [3.0, 0.0]])
        tests.append({"name": "test_forward_2d", "passed": True, "error": None})
    except Exception as e:
        tests.append({"name": "test_forward_2d", "passed": False, "error": str(e)})

    try:
        x = np.array([-2.0, 0.0, 3.0])
        grad_out = np.array([1.0, 1.0, 1.0])
        result = relu_backward(grad_out, x)
        np.testing.assert_allclose(result, [0.0, 0.0, 1.0])
        tests.append({"name": "test_backward_kills_nonpositive_gradient", "passed": True, "error": None})
    except Exception as e:
        tests.append({"name": "test_backward_kills_nonpositive_gradient", "passed": False, "error": str(e)})

    try:
        x = np.array([1.0, -1.0, 2.0, -2.0])
        grad_out = np.array([0.5, 0.5, 2.0, 2.0])
        result = relu_backward(grad_out, x)
        np.testing.assert_allclose(result, [0.5, 0.0, 2.0, 0.0])
        tests.append({"name": "test_backward_scales_by_upstream_gradient", "passed": True, "error": None})
    except Exception as e:
        tests.append({"name": "test_backward_scales_by_upstream_gradient", "passed": False, "error": str(e)})

    return tests
