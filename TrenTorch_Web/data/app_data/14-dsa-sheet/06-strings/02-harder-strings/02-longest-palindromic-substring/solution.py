def longest_palindromic_substring(s):
    t = "#" + "#".join(s) + "#"
    n = len(t)
    radius = [0] * n
    centre = right = 0
    best_len = best_centre = 0
    for i in range(n):
        if i < right:
            radius[i] = min(right - i, radius[2 * centre - i])
        while (
            i - radius[i] - 1 >= 0
            and i + radius[i] + 1 < n
            and t[i - radius[i] - 1] == t[i + radius[i] + 1]
        ):
            radius[i] += 1
        if i + radius[i] > right:
            centre, right = i, i + radius[i]
        if radius[i] > best_len:
            best_len, best_centre = radius[i], i
    start = (best_centre - best_len) // 2
    return s[start : start + best_len]
