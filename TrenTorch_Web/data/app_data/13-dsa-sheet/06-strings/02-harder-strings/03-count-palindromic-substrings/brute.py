def count_palindromic_substrings(s):
    count = 0
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            part = s[i:j]
            if all(part[k] == part[-1 - k] for k in range(len(part) // 2)):
                count += 1
    return count
