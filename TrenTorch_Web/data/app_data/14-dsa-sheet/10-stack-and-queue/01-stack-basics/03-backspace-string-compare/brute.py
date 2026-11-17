def backspace_compare(s, t):
    def typed(keys):
        text = ""
        for ch in keys:
            text = text[:-1] if ch == "#" else text + ch
        return text

    return typed(s) == typed(t)
