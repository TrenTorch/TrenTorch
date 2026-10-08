def ou_step(x, theta, sigma, dt, z):
    return x + theta * (0.0 - x) * dt + sigma * (dt**0.5) * z
