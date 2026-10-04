import numpy as np

def solve(tree_preds, oob_masks, n):
    """Implement oob accuracy according to the contract."""
    votes = []
    for i in range(n):
        v = [pred[i] for pred, mask in zip(tree_preds, oob_masks) if mask[i]]
        if v:
            u, c = np.unique(v, return_counts=True)
            votes.append(u[np.argmax(c)])
        else:
            votes.append(None)
    return votes
