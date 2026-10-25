def find_needle(haystack, needle):
    if not needle:
        return 0
    fail = [0] * len(needle)
    k = 0
    for i in range(1, len(needle)):
        while k and needle[i] != needle[k]:
            k = fail[k - 1]
        if needle[i] == needle[k]:
            k += 1
        fail[i] = k
    k = 0
    for i, ch in enumerate(haystack):
        while k and ch != needle[k]:
            k = fail[k - 1]
        if ch == needle[k]:
            k += 1
        if k == len(needle):
            return i - k + 1
    return -1
