def distinct_permutations(s):
    out = set()

    def build(rest, prefix):
        if not rest:
            out.add(prefix)
            return
        for i in range(len(rest)):
            build(rest[:i] + rest[i + 1 :], prefix + rest[i])

    build(s, "")
    return sorted(out)
