import numpy as np

def solve(predictions,weights):
        P=np.asarray(predictions,float); w=np.asarray(weights,float) if 'weights' in locals() else None
        return P.mean(0) if w is None else (w/w.sum())@P
