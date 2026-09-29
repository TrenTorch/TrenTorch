import numpy as np


def closed_form_linear_regression(input: np.ndarray, target: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Solves linear regression EXACTLY, in one shot, via the Normal
    Equation, no gradient descent, no learning rate, no epochs.

    Augment `input` with a column of ones (folding the bias into the
    weight vector as one extra coefficient), then solve for the
    combined (weight, bias) vector using the pseudoinverse (np.linalg.pinv,
    more numerically robust than a literal matrix inverse, see Theory
    for why).

    Returns (weight, bias) in the same (1, in_features)/(1,) shapes
    Full Linear Regression Training Loop's gradient-descent version
    returns, so both are drop-in interchangeable.
    """
    pass
