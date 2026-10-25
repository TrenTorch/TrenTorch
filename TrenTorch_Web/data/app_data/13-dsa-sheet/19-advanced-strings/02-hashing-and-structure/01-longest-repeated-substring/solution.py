def longest_repeated_length(s):
    n = len(s)
    mod = (1 << 61) - 1
    base = 911382323
    codes = [ord(c) for c in s]

    def has_repeat(length):
        power = pow(base, length - 1, mod)
        h = 0
        for i in range(length):
            h = (h * base + codes[i]) % mod
        seen = {h}
        for i in range(length, n):
            h = ((h - codes[i - length] * power) * base + codes[i]) % mod
            if h in seen:
                return True
            seen.add(h)
        return False

    lo, hi = 0, n - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if has_repeat(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo if n else 0
