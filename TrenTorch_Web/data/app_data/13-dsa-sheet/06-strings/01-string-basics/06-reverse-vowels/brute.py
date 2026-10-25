def reverse_vowels(s):
    chars = list(s)
    i, j = 0, len(chars) - 1
    while i < j:
        if chars[i] not in "aeiouAEIOU":
            i += 1
        elif chars[j] not in "aeiouAEIOU":
            j -= 1
        else:
            chars[i], chars[j] = chars[j], chars[i]
            i += 1
            j -= 1
    return "".join(chars)
