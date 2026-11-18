def repeated_dna(s):
    counts = {}
    for i in range(len(s) - 9):
        part = s[i : i + 10]
        counts[part] = counts.get(part, 0) + 1
    return sorted(part for part, count in counts.items() if count > 1)
