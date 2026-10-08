def ou_step(x, theta, sigma, dt, z):
    """
    x: current noise value
    theta: mean-reversion rate (non-negative)
    sigma: noise scale (non-negative)
    dt: time step (positive)
    z: a standard normal draw

    Returns:
        The next Ornstein-Uhlenbeck noise value, using the Euler-Maruyama update.
    """
    # TODO: Apply the mean-reverting drift and the scaled noise (see Theory).
    pass
