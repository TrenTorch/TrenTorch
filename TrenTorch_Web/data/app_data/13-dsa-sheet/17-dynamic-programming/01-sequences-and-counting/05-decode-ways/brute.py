def num_decodings(s):
    if not s:
        return 0

    def go(i):
        if i == len(s):
            return 1
        if s[i] == "0":
            return 0
        total = go(i + 1)
        if i + 1 < len(s) and 10 <= int(s[i : i + 2]) <= 26:
            total += go(i + 2)
        return total

    return go(0) % (10**9 + 7)
