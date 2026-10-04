import numpy as np
from pathlib import Path

_module = __import__(Path(__file__).stem.replace("-", "_").replace("tests", "solution"))
forward_pass = _module.forward_pass


def test_single_layer():
    """Single layer network (linear regression)."""
    state = [1.0, 2.0, 3.0]
    weights = [[0.5, -0.5, 1.0]]
    biases = [[0.1]]

    value = forward_pass(state, weights, biases)

    # 0.5*1 - 0.5*2 + 1.0*3 + 0.1 = 2.6
    assert np.isclose(value, 2.6)


def test_two_layer_network():
    """Two-layer network with ReLU."""
    state = [1.0]
    # First layer: 1 -> 2
    weights = [
        [[1.0], [-1.0]],  # 2x1 matrix
        [[1.0, 1.0]]       # 1x2 matrix
    ]
    biases = [
        [0.0, 0.0],
        [0.0]
    ]

    value = forward_pass(state, weights, biases)

    # Hidden: [1, -1] after ReLU: [1, 0]
    # Output: 1*1 + 1*0 = 1
    assert np.isclose(value, 1.0)


def test_deep_network():
    """Deep network with multiple hidden layers."""
    state = [1.0, 1.0]
    # 2 -> 3 -> 2 -> 1
    weights = [
        np.ones((3, 2)),
        np.ones((2, 3)),
        np.ones((1, 2))
    ]
    biases = [
        np.zeros(3),
        np.zeros(2),
        np.zeros(1)
    ]

    value = forward_pass(state, weights, biases)

    # Pass through: [1,1] -> [2,2,2] after ReLU
    # -> [6, 6] after ReLU
    # -> [12]
    assert isinstance(value, float)


def test_relu_activation():
    """ReLU correctly removes negative values."""
    state = [1.0]
    # This network should output negative before final layer
    weights = [
        [[-1.0]],  # Make hidden negative
        [[1.0]]
    ]
    biases = [[0.0], [0.0]]

    value = forward_pass(state, weights, biases)

    # Hidden: -1 after ReLU: 0
    # Output: 0
    assert np.isclose(value, 0.0)


def test_batch_dimensions():
    """Network handles correct dimensions."""
    state = np.random.randn(5)
    weights = [np.random.randn(10, 5), np.random.randn(8, 10), np.random.randn(1, 8)]
    biases = [np.random.randn(10), np.random.randn(8), np.random.randn(1)]

    value = forward_pass(state, weights, biases)

    assert isinstance(value, float)
