def longest_repeated_length(s):
    for length in range(len(s) - 1, 0, -1):
        seen = set()
        for i in range(len(s) - length + 1):
            part = s[i : i + length]
            if part in seen:
                return length
            seen.add(part)
    return 0
