import numpy as np


def pad_batch(seqs, pad_id, max_len=None, side="right"):
    if side not in ("right", "left"):
        raise ValueError(f"bad side: {side}")
    target = max_len if max_len is not None else max(len(s) for s in seqs)
    ids = np.full((len(seqs), target), pad_id, dtype=np.int64)
    mask = np.zeros((len(seqs), target), dtype=np.int64)
    for i, s in enumerate(seqs):
        s = s[:target]
        n = len(s)
        if side == "right":
            ids[i, :n], mask[i, :n] = s, 1
        else:
            ids[i, target - n:], mask[i, target - n:] = s, 1
    return ids, mask
