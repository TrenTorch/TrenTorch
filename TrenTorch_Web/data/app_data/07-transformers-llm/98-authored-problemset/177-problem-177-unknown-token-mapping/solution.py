import numpy as np

def solve(tokens, vocab, unk_id):
    """Implement unknown token mapping according to the contract."""
    return [vocab.get(tok, unk_id) for tok in tokens]
