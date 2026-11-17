def matrix_chain_cost(dims):
    n = len(dims)
    if n < 3:
        return 0
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):
        for i in range(n - length):
            j = i + length
            best = float("inf")
            for k in range(i + 1, j):
                value = dp[i][k] + dp[k][j] + dims[i] * dims[k] * dims[j]
                if value < best:
                    best = value
            dp[i][j] = best
    return dp[0][n - 1]
