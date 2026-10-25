def max_nesting_depth(s):
    best = 0
    for i in range(len(s) + 1):
        prefix = s[:i]
        best = max(best, prefix.count("(") - prefix.count(")"))
    return best
