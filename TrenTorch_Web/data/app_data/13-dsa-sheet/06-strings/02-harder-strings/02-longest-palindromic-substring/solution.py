def longest_palindromic_substring(s):
    n = len(s)
    best_start, best_len = 0, 0
    for center in range(2 * n - 1):
        left = center // 2
        right = left + center % 2
        while left >= 0 and right < n and s[left] == s[right]:
            left -= 1
            right += 1
        length = right - left - 1
        if length > best_len:
            best_start, best_len = left + 1, length
    return s[best_start : best_start + best_len]
