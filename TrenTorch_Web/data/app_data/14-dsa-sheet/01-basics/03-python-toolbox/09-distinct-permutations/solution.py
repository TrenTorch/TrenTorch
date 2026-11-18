from collections import Counter


def distinct_permutations(s):
    letters = sorted(Counter(s).items())
    left = [count for _, count in letters]
    n = len(s)
    out = []
    prefix = []

    def build():
        if len(prefix) == n:
            out.append("".join(prefix))
            return
        for i, (ch, _) in enumerate(letters):
            if left[i]:
                left[i] -= 1
                prefix.append(ch)
                build()
                prefix.pop()
                left[i] += 1

    build()
    return out
