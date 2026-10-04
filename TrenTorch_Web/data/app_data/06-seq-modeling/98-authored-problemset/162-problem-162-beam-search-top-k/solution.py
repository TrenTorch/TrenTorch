import numpy as np

def solve(step_scores, k):
    """Implement beam search top-k according to the contract."""
    beams = [([], 0.0)]
    for scores in step_scores:
        cand = []
        for seq, sc in beams:
            for tok, lp in enumerate(scores):
                cand.append((seq + [tok], sc + lp))
        beams = sorted(cand, key=lambda z: z[1], reverse=True)[:k]
    return beams
