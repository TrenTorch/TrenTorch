def slow_trajectory(phi0, fast_points, alpha):
    out = []
    phi = phi0
    for f in fast_points:
        phi = phi + alpha * (f - phi)
        out.append(phi)
    return out
