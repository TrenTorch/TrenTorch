def min_cut_palindromes(s):
    n = len(s)
    if n == 0:
        return 0
    cuts = list(range(-1, n))  # cuts[i]: fewest cuts for the first i letters
    for centre in range(n):
        for left, right in ((centre, centre), (centre, centre + 1)):
            while left >= 0 and right < n and s[left] == s[right]:
                if cuts[left] + 1 < cuts[right + 1]:
                    cuts[right + 1] = cuts[left] + 1
                left -= 1
                right += 1
    return cuts[n]
