def word_pattern(pattern, words):
    if len(pattern) != len(words):
        return False
    return [pattern.index(c) for c in pattern] == [words.index(w) for w in words]
