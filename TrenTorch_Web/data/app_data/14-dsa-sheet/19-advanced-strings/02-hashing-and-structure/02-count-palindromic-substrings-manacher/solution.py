def count_palindromes_fast(s):
    n = len(s)
    total = 0
    d1 = [0] * n
    left, right = 0, -1
    for i in range(n):
        k = 1 if i > right else min(d1[left + right - i], right - i + 1)
        while i - k >= 0 and i + k < n and s[i - k] == s[i + k]:
            k += 1
        d1[i] = k
        total += k
        if i + k - 1 > right:
            left, right = i - k + 1, i + k - 1
    d2 = [0] * n
    left, right = 0, -1
    for i in range(n):
        k = 0 if i > right else min(d2[left + right - i + 1], right - i + 1)
        while i - k - 1 >= 0 and i + k < n and s[i - k - 1] == s[i + k]:
            k += 1
        d2[i] = k
        total += k
        if i + k - 1 > right:
            left, right = i - k, i + k - 1
    return total
