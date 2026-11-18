def longest_happy_prefix(s):
    for length in range(len(s) - 1, 0, -1):
        if s[:length] == s[len(s) - length :]:
            return s[:length]
    return ""
