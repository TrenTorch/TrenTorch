def compress_runs(s):
    out = ""
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        out += s[i] + (str(j - i) if j - i > 1 else "")
        i = j
    return out
