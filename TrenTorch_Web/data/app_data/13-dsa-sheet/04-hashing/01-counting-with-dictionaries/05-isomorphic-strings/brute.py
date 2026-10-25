def isomorphic_strings(s, t):
    if len(s) != len(t):
        return False

    def pattern(text):
        return [text.index(ch) for ch in text]

    return pattern(s) == pattern(t)
