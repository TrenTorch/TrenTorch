def group_anagrams(words):
    remaining = list(words)
    groups = []
    while remaining:
        first = remaining[0]
        group = [w for w in remaining if sorted(w) == sorted(first)]
        remaining = [w for w in remaining if sorted(w) != sorted(first)]
        groups.append(sorted(group))
    return sorted(groups)
