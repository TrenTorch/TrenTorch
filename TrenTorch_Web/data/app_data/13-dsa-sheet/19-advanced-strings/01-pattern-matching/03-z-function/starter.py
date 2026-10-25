def z_function(s: str) -> list[int]:
    """For every position, return the length of the longest common prefix of s and the suffix starting there."""
    # This is correct but too slow: it compares the two strings letter by letter at every position.
    z = [0] * len(s)
    for i in range(1, len(s)):
        while i + z[i] < len(s) and s[z[i]] == s[i + z[i]]:
            z[i] += 1
    return z
