from itertools import combinations


def longest_palindrome_subseq(s):
    for size in range(len(s), 0, -1):
        for positions in combinations(range(len(s)), size):
            text = "".join(s[i] for i in positions)
            if text == text[::-1]:
                return size
    return 0
