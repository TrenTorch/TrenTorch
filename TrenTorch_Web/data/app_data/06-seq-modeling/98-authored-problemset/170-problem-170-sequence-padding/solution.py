import numpy as np

def solve(sequences, pad_id=0, max_length=None):
    """Implement sequence padding according to the contract."""
    sequences = [list(s) for s in sequences]
    length = max_length if max_length is not None else max(map(len, sequences), default=0)
    out = np.full((len(sequences), length), pad_id, dtype=int)
    for i, seq in enumerate(sequences):
        out[i, :min(len(seq), length)] = seq[:length]
    return out
