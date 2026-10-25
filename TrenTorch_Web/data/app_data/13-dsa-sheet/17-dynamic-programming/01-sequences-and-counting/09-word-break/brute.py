def word_break(s, words):
    dictionary = set(words)

    def go(start):
        if start == len(s):
            return True
        return any(
            s[start:end] in dictionary and go(end)
            for end in range(start + 1, len(s) + 1)
        )

    return go(0)
