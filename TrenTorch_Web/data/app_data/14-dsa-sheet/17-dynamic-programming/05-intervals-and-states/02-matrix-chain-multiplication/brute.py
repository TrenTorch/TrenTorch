def matrix_chain_cost(dims):
    def go(i, j):
        if j - i <= 1:
            return 0
        return min(
            go(i, k) + go(k, j) + dims[i] * dims[k] * dims[j] for k in range(i + 1, j)
        )

    return go(0, len(dims) - 1) if len(dims) > 1 else 0
