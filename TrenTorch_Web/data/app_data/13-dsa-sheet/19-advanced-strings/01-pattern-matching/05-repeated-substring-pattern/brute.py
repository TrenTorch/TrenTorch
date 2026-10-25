def repeated_substring_pattern(s):
    n = len(s)
    return any(n % k == 0 and s == s[:k] * (n // k) for k in range(1, n // 2 + 1))
