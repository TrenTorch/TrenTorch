def reverse_vowels(s):
    vowels = [ch for ch in s if ch in "aeiouAEIOU"]
    replacement = iter(reversed(vowels))
    return "".join(next(replacement) if ch in "aeiouAEIOU" else ch for ch in s)
