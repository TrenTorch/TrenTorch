def word_break(s, words):
    dictionary = set(words)
    maxlen = max((len(w) for w in dictionary), default=0)
    can = [True] + [False] * len(s)
    for i in range(1, len(s) + 1):
        for j in range(max(0, i - maxlen), i):
            if can[j] and s[j:i] in dictionary:
                can[i] = True
                break
    return can[len(s)]
