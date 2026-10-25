def max_coins(nums):
    a = [1] + nums + [1]
    n = len(a)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):
        for i in range(n - length):
            j = i + length
            best = 0
            for k in range(i + 1, j):
                value = dp[i][k] + dp[k][j] + a[i] * a[k] * a[j]
                if value > best:
                    best = value
            dp[i][j] = best
    return dp[0][n - 1]
