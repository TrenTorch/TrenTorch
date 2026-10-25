def replace_words(roots, sentence):
    out = []
    for word in sentence.split():
        best = word
        for root in roots:
            if word.startswith(root) and len(root) < len(best):
                best = root
        out.append(best)
    return " ".join(out)
