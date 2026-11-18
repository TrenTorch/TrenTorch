def repeated_dna(s: str) -> list[str]:
    """Return every 10-letter sequence that occurs more than once, sorted."""
    # This is correct but too slow: it counts the occurrences of every sequence by scanning the whole string.
    found = set()
    for i in range(len(s) - 9):
        part = s[i : i + 10]
        if sum(1 for j in range(len(s) - 9) if s.startswith(part, j)) > 1:
            found.add(part)
    return sorted(found)
