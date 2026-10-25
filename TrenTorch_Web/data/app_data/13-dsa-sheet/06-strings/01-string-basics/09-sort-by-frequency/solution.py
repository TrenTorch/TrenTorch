from collections import Counter


def sort_by_frequency(s):
    counts = Counter(s)
    order = sorted(counts, key=lambda ch: (-counts[ch], ch))
    return "".join(ch * counts[ch] for ch in order)
