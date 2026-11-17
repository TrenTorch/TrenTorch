import numpy as np

def solve(predictions,targets):
        return float(np.mean([a.strip()==b.strip() for a,b in zip(predictions,targets)]))
