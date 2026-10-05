def taylor_first_order(f, f_prime, a, x):
    return f(a) + f_prime(a) * (x - a)


def taylor_second_order(f, f_prime, f_double_prime, a, x):
    return taylor_first_order(f, f_prime, a, x) + (f_double_prime(a) / 2) * (x - a) ** 2
