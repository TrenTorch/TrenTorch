def shortest_palindrome(s: str) -> str:
    """Add the fewest letters in front of s to make a palindrome."""
    # This is correct but too slow: it checks every prefix for being a palindrome.
    for k in range(len(s), 0, -1):
        if all(s[i] == s[k - 1 - i] for i in range(k // 2)):
            return s[k:][::-1] + s
    return s
