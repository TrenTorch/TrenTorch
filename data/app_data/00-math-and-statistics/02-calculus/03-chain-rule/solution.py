def compose(f, g):
    return lambda x: f(g(x))


def chain_rule_derivative(f_prime, g, g_prime, x: float) -> float:
    return f_prime(g(x)) * g_prime(x)
