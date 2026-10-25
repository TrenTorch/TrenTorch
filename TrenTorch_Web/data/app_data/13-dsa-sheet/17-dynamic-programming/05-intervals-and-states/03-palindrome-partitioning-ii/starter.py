def min_cut_palindromes(s: str) -> int:
    """Return the fewest cuts that split s into palindromes."""

    # This is correct but too slow: it re-checks every piece for being a palindrome and solves the same suffixes again.
    def go(start):
        if start == len(s):
            return -1
        return min(
            1 + go(end)
            for end in range(start + 1, len(s) + 1)
            if s[start:end] == s[start:end][::-1]
        )

    return go(0) if s else 0
