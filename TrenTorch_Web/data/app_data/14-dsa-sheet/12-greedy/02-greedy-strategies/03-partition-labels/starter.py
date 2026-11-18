def partition_labels(s: str) -> list[int]:
    """Cut the string into as many parts as possible so each letter is in one part."""
    # This is correct but too slow: at every cut it compares the letters on both sides.
    sizes = []
    start = 0
    for i in range(1, len(s) + 1):
        if i == len(s) or not set(s[start:i]) & set(s[i:]):
            sizes.append(i - start)
            start = i
    return sizes
