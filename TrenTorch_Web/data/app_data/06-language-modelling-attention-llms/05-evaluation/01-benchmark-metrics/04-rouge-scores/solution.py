from collections import Counter


def _f1(p, r):
    return 0.0 if p + r == 0 else 2 * p * r / (p + r)


def _ngrams(tokens, n):
    return Counter(tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1))


def rouge_n(candidate, reference, n):
    c, r = _ngrams(candidate, n), _ngrams(reference, n)
    overlap = sum((c & r).values())
    p = overlap / sum(c.values()) if sum(c.values()) else 0.0
    rec = overlap / sum(r.values()) if sum(r.values()) else 0.0
    return p, rec, _f1(p, rec)


def rouge_l(candidate, reference):
    m, k = len(candidate), len(reference)
    dp = [[0] * (k + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, k + 1):
            if candidate[i - 1] == reference[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    lcs = dp[m][k]
    p = lcs / m if m else 0.0
    r = lcs / k if k else 0.0
    return p, r, _f1(p, r)
