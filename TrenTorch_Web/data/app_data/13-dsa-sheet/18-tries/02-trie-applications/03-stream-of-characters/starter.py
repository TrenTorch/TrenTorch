def stream_checker(words: list[str], stream: str) -> list[bool]:
    """After each letter, report whether a suffix of the stream is a word."""
    # This is correct but too slow: it tries every word as a suffix after every letter.
    out = []
    for i in range(1, len(stream) + 1):
        out.append(any(stream[:i].endswith(w) for w in words))
    return out
