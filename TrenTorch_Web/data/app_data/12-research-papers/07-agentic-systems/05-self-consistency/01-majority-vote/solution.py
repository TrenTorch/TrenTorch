def majority_vote(answers):
    counts = {}
    for a in answers:
        counts[a] = counts.get(a, 0) + 1
    best = None
    for a in answers:
        if best is None or counts[a] > counts[best]:
            best = a
    return best
