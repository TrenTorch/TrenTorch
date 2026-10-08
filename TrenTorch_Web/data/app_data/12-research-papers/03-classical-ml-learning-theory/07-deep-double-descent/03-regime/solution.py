def double_descent_regime(n, p):
    if p < n:
        return "underparameterized"
    if p == n:
        return "interpolation"
    return "overparameterized"
