import numpy as np


def circuit_output(x: np.ndarray, theta: np.ndarray, n: int, L: int) -> float:
    """
    Simulates the fixed hardware-efficient variational circuit exactly
    (real-valued state vector, no complex arithmetic needed) and returns
    the Pauli-Z expectation value on qubit 0.

    Circuit, starting from |0...0>:
      1. Encoding layer: for i = 0..n-1, apply RY(x[i]) to qubit i.
      2. For each layer l = 0..L-1:
         a. Entangling chain: for i = 0..n-2, apply CNOT(control=i,
            target=i+1), in increasing order of i. (Empty when n == 1.)
         b. Rotation layer: for i = 0..n-1, apply RY(theta[l, i]) to
            qubit i.

    RY(t) = [[cos(t/2), -sin(t/2)], [sin(t/2), cos(t/2)]] acting on one
    qubit. CNOT(control, target): flips target iff control is |1>.

    Measurement: p = P(qubit 0 = |0>) - P(qubit 0 = |1>), the exact
    expectation of Z on qubit 0 -- always in [-1, 1].

    x: shape (n,). theta: shape (L, n) (theta[l, i] is layer l's angle
    for qubit i). Returns a single float.
    """
    pass


def train_and_predict(
    X: np.ndarray,
    y: np.ndarray,
    n: int,
    L: int,
    theta_init: np.ndarray,
    eta: float,
    T: int,
    queries: np.ndarray,
) -> np.ndarray:
    """
    Trains the circuit's L*n parameters with T steps of full-batch
    gradient descent on mean squared error, using the parameter-shift
    rule for exact gradients, then predicts on every row of `queries`.

    Loss(theta) = mean_i( (circuit_output(x_i, theta, n, L) - y_i)^2 )

    Parameter-shift rule (exact, no approximation): for any theta[l, i],

        d p(x, theta) / d theta[l, i]
            = ( p(x, theta + (pi/2)*e_{l,i}) - p(x, theta - (pi/2)*e_{l,i}) ) / 2

    where e_{l,i} shifts only theta[l, i]. By the chain rule, summed
    over the training set:

        d Loss / d theta[l, i]
            = (2 / n_train) * sum_k( (p(x_k,theta) - y_k) * dp(x_k,theta)/dtheta[l,i] )

    Training loop, starting from theta_init (shape (L, n) once
    reshaped from its flattened input form), for exactly T steps:

        theta <- theta - eta * grad(Loss)(theta)

    (Gradient recomputed fresh from the full training set at every
    step.) T = 0 means: skip training, predict directly with
    theta_init unchanged.

    X: shape (n_train, n). y: shape (n_train,).
    theta_init: shape (L, n) or any array reshapeable to it.
    eta: learning rate (> 0). T: number of gradient steps (>= 0).
    queries: shape (m, n).
    Returns predictions, shape (m,).
    """
    pass
