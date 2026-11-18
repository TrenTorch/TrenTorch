def longest_valid_parentheses(s):
    best = 0
    for i in range(len(s)):
        depth = 0
        for j in range(i, len(s)):
            depth += 1 if s[j] == "(" else -1
            if depth < 0:
                break
            if depth == 0:
                best = max(best, j - i + 1)
    return best
