def lcs_length(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[-1][-1]


def trajectory_match(actual, reference):
    lcs = lcs_length(actual, reference)
    precision = lcs / len(actual) if actual else 0.0
    recall = lcs / len(reference) if reference else 0.0
    return precision, recall, lcs == len(reference)
