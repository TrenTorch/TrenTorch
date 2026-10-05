def pass_hat_k(n, c, k):
    if c < k:
        return 0.0
    result = 1.0
    for i in range(k):
        result *= (c - i) / (n - i)
    return result


def mean_pass_hat_k(ns, cs, k):
    return sum(pass_hat_k(n, c, k) for n, c in zip(ns, cs)) / len(ns)
