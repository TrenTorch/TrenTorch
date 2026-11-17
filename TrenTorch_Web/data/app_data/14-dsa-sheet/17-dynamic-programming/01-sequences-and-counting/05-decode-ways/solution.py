def num_decodings(s):
    mod = 10**9 + 7
    a, b = 1, 1
    for i in range(1, len(s) + 1):
        now = 0
        if s[i - 1] != "0":
            now += b
        if i >= 2 and "10" <= s[i - 2 : i] <= "26":
            now += a
        a, b = b, now % mod
    return b % mod if s else 0
