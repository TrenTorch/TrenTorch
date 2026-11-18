def run_word_dictionary(ops):
    words = set()
    out = []
    for op in ops:
        kind, text = op.split()
        if kind == "add":
            words.add(text)
        else:
            out.append(
                any(
                    len(w) == len(text) and all(p in (".", c) for p, c in zip(text, w))
                    for w in words
                )
            )
    return out
