def agreement_rate(answers):
    counts = {}
    for a in answers:
        counts[a] = counts.get(a, 0) + 1
    return max(counts.values()) / len(answers)
