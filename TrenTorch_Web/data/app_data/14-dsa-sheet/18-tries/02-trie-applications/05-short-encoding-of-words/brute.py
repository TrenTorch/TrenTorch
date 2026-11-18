def minimum_length_encoding(words):
    unique = set(words)
    keep = [
        w
        for w in unique
        if not any(other != w and other.endswith(w) for other in unique)
    ]
    return sum(len(w) + 1 for w in keep)
