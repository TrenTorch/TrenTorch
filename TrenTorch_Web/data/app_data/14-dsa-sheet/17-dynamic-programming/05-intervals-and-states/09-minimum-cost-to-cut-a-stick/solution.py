def min_cost_cut(length, cuts):
    points = [0] + sorted(cuts) + [length]
    n = len(points)
    dp = [[0] * n for _ in range(n)]
    best_cut = [[0] * n for _ in range(n)]
    for i in range(n - 1):
        best_cut[i][i + 1] = i + 1
    for span in range(2, n):
        for i in range(n - span):
            j = i + span
            low = max(i + 1, best_cut[i][j - 1])
            high = min(j - 1, best_cut[i + 1][j])
            best = None
            for k in range(low, high + 1):
                value = dp[i][k] + dp[k][j]
                if best is None or value < best:
                    best, best_cut[i][j] = value, k
            dp[i][j] = best + points[j] - points[i]
    return dp[0][n - 1]
