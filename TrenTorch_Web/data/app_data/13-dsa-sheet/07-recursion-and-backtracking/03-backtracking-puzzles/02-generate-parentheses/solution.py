def generate_parentheses(n):
    out = []

    def go(prefix, opens, closes):
        if len(prefix) == 2 * n:
            out.append(prefix)
            return
        if opens < n:
            go(prefix + "(", opens + 1, closes)
        if closes < opens:
            go(prefix + ")", opens, closes + 1)

    go("", 0, 0)
    return out
