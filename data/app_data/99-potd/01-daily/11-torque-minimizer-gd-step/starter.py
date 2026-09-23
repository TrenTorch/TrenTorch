def gd_step(a: float, b: float, c: float, theta_0: float, eta: float) -> tuple[float, float]:
    """
    One gradient-descent step on C(theta) = a*theta^2 + b*theta + c.

    dC/dtheta = 2*a*theta + b. Take theta_1 = theta_0 - eta * dC/dtheta(theta_0).

    Return (theta_1, C(theta_1)). A single closed-form computation, no
    iteration. a can be negative (a concave cost); still just report the
    mechanical result of one step.
    """
    # TODO: substitute theta_0 into the gradient formula, then evaluate C at theta_1.
    pass
