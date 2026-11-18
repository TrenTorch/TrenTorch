def longest_palindromic_substring(s):
    best = ""
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            part = s[i:j]
            if all(part[k] == part[-1 - k] for k in range(len(part) // 2)) and len(
                part
            ) > len(best):
                best = part
    return best
