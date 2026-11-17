def count_overlapping(text, pattern):
    return sum(
        1 for i in range(len(text) - len(pattern) + 1) if text.startswith(pattern, i)
    )
