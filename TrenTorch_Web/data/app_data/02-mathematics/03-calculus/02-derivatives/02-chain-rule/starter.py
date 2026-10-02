def compose(f, g):
    """
    Returns a new function h(x) = f(g(x)), applying g first, then f.
    """
    pass


def chain_rule_derivative(f_prime, g, g_prime, x: float) -> float:
    """
    For h(x) = f(g(x)), the chain rule says:

        h'(x) = f'(g(x)) * g'(x)

    "the derivative of the outside function, evaluated at the inside
    function's value, times the derivative of the inside function."

    f_prime, g, g_prime are all already-known functions (f itself is
    not needed here, only its derivative f_prime).
    """
    pass
