from itertools import product


def generate_parentheses(n):
    out = []
    for chars in product("()", repeat=2 * n):
        depth = 0
        for ch in chars:
            depth += 1 if ch == "(" else -1
            if depth < 0:
                break
        else:
            if depth == 0:
                out.append("".join(chars))
    return sorted(out)
