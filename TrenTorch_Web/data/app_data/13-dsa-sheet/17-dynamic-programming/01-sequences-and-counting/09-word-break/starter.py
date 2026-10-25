def word_break(s: str, words: list[str]) -> bool:
    """Return True if s can be split into words from the list."""
    # This is correct but too slow: it tries every split again and again.
    dictionary = set(words)

    def go(start):
        if start == len(s):
            return True
        return any(
            s[start:end] in dictionary and go(end)
            for end in range(start + 1, len(s) + 1)
        )

    return go(0)
