def palindrome_pairs(words: list[str]) -> list[list[int]]:
    """Return every pair of indices whose words join into a palindrome."""
    # This is correct but too slow: it tests every pair of words.
    out = []
    for i in range(len(words)):
        for j in range(len(words)):
            if i != j:
                s = words[i] + words[j]
                if s == s[::-1]:
                    out.append([i, j])
    return out
