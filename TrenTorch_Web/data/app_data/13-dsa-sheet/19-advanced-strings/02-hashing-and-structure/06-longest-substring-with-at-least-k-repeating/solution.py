def longest_substring_k_repeating(s, k):
    def solve(lo, hi):
        if hi - lo < k:
            return 0
        counts = {}
        for i in range(lo, hi):
            counts[s[i]] = counts.get(s[i], 0) + 1
        rare = {ch for ch, c in counts.items() if c < k}
        if not rare:
            return hi - lo
        best = 0
        start = lo
        for i in range(lo, hi + 1):
            if i == hi or s[i] in rare:
                best = max(best, solve(start, i))
                start = i + 1
        return best

    return solve(0, len(s))
