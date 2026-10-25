def replace_words(roots: list[str], sentence: str) -> str:
    """Replace each word of the sentence by its shortest root, if any."""
    # This is correct but too slow: it tries every root for every word.
    out = []
    for word in sentence.split():
        best = word
        for root in roots:
            if word.startswith(root) and len(root) < len(best):
                best = root
        out.append(best)
    return " ".join(out)
