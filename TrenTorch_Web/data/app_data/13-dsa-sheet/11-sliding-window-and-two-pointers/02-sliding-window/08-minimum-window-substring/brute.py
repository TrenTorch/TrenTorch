from collections import Counter


def min_window(s, t):
    if not t:
        return ""
    need = Counter(t)
    best = ""
    for i in range(len(s)):
        for j in range(i, len(s)):
            window = Counter(s[i : j + 1])
            if all(window[c] >= n for c, n in need.items()):
                if best == "" or j - i + 1 < len(best):
                    best = s[i : j + 1]
    return best
