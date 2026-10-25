def remove_outer_parentheses(s):
    out = ""
    start = depth = 0
    for i, ch in enumerate(s):
        depth += 1 if ch == "(" else -1
        if depth == 0:
            out += s[start + 1 : i]
            start = i + 1
    return out
