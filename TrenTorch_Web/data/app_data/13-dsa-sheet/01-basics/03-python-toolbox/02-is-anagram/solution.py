from collections import Counter


def is_anagram(a, b):
    return len(a) == len(b) and Counter(a) == Counter(b)
