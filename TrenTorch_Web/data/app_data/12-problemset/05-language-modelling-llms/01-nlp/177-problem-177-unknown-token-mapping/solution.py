import numpy as np

def solve(tokens,vocab,unk_id):
        return [vocab.get(tok,unk_id) for tok in tokens]
