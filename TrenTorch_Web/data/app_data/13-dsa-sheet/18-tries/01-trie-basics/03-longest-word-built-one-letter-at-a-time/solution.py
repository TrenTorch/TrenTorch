def longest_word(words):
    built = {""}
    best = ""
    for word in sorted(set(words)):
        if word[:-1] in built:
            built.add(word)
            if len(word) > len(best):
                best = word
    return best
