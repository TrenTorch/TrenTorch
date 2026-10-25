def backspace_compare(s, t):
    def typed(keys):
        out = []
        for ch in keys:
            if ch != "#":
                out.append(ch)
            elif out:
                out.pop()
        return out

    return typed(s) == typed(t)
