from math import factorial


def kth_permutation(n, k):
    remaining = list(range(1, n + 1))
    k -= 1
    out = []
    for size in range(n - 1, -1, -1):
        index, k = divmod(k, factorial(size))
        out.append(str(remaining.pop(index)))
    return "".join(out)
