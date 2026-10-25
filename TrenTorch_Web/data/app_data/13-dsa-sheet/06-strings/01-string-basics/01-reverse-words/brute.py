def reverse_words(s):
    words = []
    current = ""
    for ch in s + " ":
        if ch == " ":
            if current:
                words.append(current)
            current = ""
        else:
            current += ch
    out = ""
    for word in reversed(words):
        out = out + (" " if out else "") + word
    return out
