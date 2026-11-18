from itertools import product


def check_valid_string(s):
    stars = [i for i, ch in enumerate(s) if ch == "*"]
    for choice in product("()_", repeat=len(stars)):
        text = list(s)
        for i, c in zip(stars, choice):
            text[i] = c
        depth = 0
        for ch in text:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth < 0:
                    break
        else:
            if depth == 0:
                return True
    return False
