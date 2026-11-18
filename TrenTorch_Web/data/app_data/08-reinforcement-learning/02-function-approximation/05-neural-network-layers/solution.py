import numpy as np


def forward_pass(state, weights, biases):
    """
    Neural network forward pass.

    Args:
        state: input state vector
        weights: list of weight matrices [W1, W2, ..., Wn]
        biases: list of bias vectors [b1, b2, ..., bn]

    Returns:
        value: scalar output (no activation on final layer)
    """
    x = np.array(state, dtype=np.float32)

    # Forward through hidden layers
    for i in range(len(weights) - 1):
        W = np.array(weights[i], dtype=np.float32)
        b = np.array(biases[i], dtype=np.float32)

        # Linear layer
        x = W @ x + b

        # ReLU activation
        x = np.maximum(0.0, x)

    # Final layer (no activation)
    W_final = np.array(weights[-1], dtype=np.float32)
    b_final = np.array(biases[-1], dtype=np.float32)
    value = W_final @ x + b_final

    return float(value[0]) if hasattr(value, '__len__') else float(value)
