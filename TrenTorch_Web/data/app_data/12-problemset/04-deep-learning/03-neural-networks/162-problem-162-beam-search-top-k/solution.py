def solve(step_scores, k):
    """Return the top k token sequences and cumulative scores after all steps."""
    if k <= 0:
        raise ValueError("k must be positive")
    beams = [((), 0.0)]
    for scores in step_scores:
        candidates = [
            (sequence + (token,), score + float(value))
            for sequence, score in beams
            for token, value in enumerate(scores)
        ]
        beams = sorted(candidates, key=lambda item: (-item[1], item[0]))[:k]
    return [(list(sequence), score) for sequence, score in beams]
