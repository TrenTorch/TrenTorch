def backspace_compare(s, t):
    def next_typed(text, i):
        skip = 0
        while i >= 0:
            if text[i] == "#":
                skip += 1
            elif skip:
                skip -= 1
            else:
                return i
            i -= 1
        return -1

    i, j = len(s) - 1, len(t) - 1
    while True:
        i = next_typed(s, i)
        j = next_typed(t, j)
        if i < 0 and j < 0:
            return True
        if i < 0 or j < 0 or s[i] != t[j]:
            return False
        i -= 1
        j -= 1
