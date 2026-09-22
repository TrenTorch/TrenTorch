def gd_step(a: float, b: float, c: float, theta_0: float, eta: float) -> tuple[float, float]:
    grad = 2 * a * theta_0 + b
    theta_1 = theta_0 - eta * grad
    cost = a * theta_1**2 + b * theta_1 + c
    return theta_1, cost
