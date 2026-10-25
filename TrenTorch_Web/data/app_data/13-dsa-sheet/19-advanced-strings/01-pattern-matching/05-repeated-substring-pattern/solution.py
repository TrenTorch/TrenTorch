def repeated_substring_pattern(s):
    n = len(s)
    if n < 2:
        return False
    pi = [0] * n
    k = 0
    for i in range(1, n):
        while k and s[i] != s[k]:
            k = pi[k - 1]
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    period = n - pi[-1]
    return pi[-1] > 0 and n % period == 0
