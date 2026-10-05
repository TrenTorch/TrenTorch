import numpy as np


def adam_minimize(grad_fn, theta0, steps, lr=0.1, beta1=0.9, beta2=0.999, eps=1e-8):
    theta = np.asarray(theta0, dtype=float)
    m = np.zeros_like(theta)
    v = np.zeros_like(theta)
    trajectory = [theta.copy()]
    for t in range(1, steps + 1):
        grad = grad_fn(theta)
        m = beta1 * m + (1 - beta1) * grad
        v = beta2 * v + (1 - beta2) * grad**2
        m_hat = m / (1 - beta1**t)
        v_hat = v / (1 - beta2**t)
        theta = theta - lr * m_hat / (np.sqrt(v_hat) + eps)
        trajectory.append(theta.copy())
    return trajectory
