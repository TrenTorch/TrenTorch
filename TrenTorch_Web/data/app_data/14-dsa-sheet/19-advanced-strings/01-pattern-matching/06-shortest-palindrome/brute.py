def shortest_palindrome(s):
    for k in range(len(s), 0, -1):
        if s[:k] == s[:k][::-1]:
            return s[k:][::-1] + s
    return s
