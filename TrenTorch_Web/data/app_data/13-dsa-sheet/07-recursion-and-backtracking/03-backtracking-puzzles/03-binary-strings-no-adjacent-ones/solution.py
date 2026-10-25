def no_adjacent_ones(n):
    out = []

    def go(prefix):
        if len(prefix) == n:
            out.append(prefix)
            return
        go(prefix + "0")
        if not prefix.endswith("1"):
            go(prefix + "1")

    go("")
    return out
