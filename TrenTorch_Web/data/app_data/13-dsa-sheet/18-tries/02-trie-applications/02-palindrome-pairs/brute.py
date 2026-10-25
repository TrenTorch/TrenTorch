def palindrome_pairs(words):
    out = []
    for i in range(len(words)):
        for j in range(len(words)):
            if i != j:
                s = words[i] + words[j]
                if s == s[::-1]:
                    out.append([i, j])
    return out
