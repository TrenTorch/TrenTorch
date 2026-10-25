def valid_palindrome_ii(s):
    if s == s[::-1]:
        return True
    return any(s[:i] + s[i + 1 :] == (s[:i] + s[i + 1 :])[::-1] for i in range(len(s)))
