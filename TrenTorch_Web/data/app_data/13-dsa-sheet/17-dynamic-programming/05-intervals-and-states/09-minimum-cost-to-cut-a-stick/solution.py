def min_cost_cut(length, cuts):
    points = [0] + sorted(cuts) + [length]
    n = len(points)
    dp = [[0] * n for _ in range(n)]
    for span in range(2, n):
        for i in range(n - span):
            j = i + span
            best = min(dp[i][k] + dp[k][j] for k in range(i + 1, j))
            dp[i][j] = best + points[j] - points[i]
    return dp[0][n - 1]
