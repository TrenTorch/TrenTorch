def longest_valid_parentheses(s):
    best = 0
    for sequence, opener in ((s, "("), (reversed(s), ")")):
        left = right = 0
        for ch in sequence:
            if ch == opener:
                left += 1
            else:
                right += 1
            if left == right:
                best = max(best, 2 * left)
            elif right > left:
                left = right = 0
    return best
