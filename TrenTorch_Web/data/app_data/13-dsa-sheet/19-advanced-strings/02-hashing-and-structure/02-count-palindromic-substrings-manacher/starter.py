def count_palindromes_fast(s: str) -> int:
    """Count the substrings that are palindromes."""
    # This is correct but too slow on long strings: it expands around every centre separately.
    n = len(s)
    count = 0
    for centre in range(2 * n - 1):
        left, right = centre // 2, centre // 2 + centre % 2
        while left >= 0 and right < n and s[left] == s[right]:
            count += 1
            left -= 1
            right += 1
    return count
