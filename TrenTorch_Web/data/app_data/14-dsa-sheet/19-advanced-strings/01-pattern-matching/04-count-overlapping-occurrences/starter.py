def count_overlapping(text: str, pattern: str) -> int:
    """Count how many times the pattern occurs in the text, overlaps included."""
    # This is correct but too slow: it compares the pattern letter by letter at every start position.
    n, m = len(text), len(pattern)
    count = 0
    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            count += 1
    return count
