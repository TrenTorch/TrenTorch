def longest_palindrome_subseq(s: str) -> int:
    """Return the length of the longest subsequence that reads the same both ways."""

    # This is correct but too slow: it solves the same substrings again and again.
    def go(i, j):
        if i > j:
            return 0
        if i == j:
            return 1
        if s[i] == s[j]:
            return 2 + go(i + 1, j - 1)
        return max(go(i + 1, j), go(i, j - 1))

    return go(0, len(s) - 1)
