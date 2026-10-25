def prefix_function(s):
    out = []
    for i in range(len(s)):
        best = 0
        for length in range(i, 0, -1):
            if s[:length] == s[i - length + 1 : i + 1]:
                best = length
                break
        out.append(best)
    return out
