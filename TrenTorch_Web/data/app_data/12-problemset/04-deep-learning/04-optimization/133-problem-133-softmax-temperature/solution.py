import numpy as np

def solve(logits, temperature):
    """Temperature scaling divides logits by a positive temperature before applying stable softmax; larger temperatures flatten the distribution."""
    logits=np.asarray(logits,dtype=float); temperature=float(temperature)
    if temperature<=0: raise ValueError("temperature must be positive")
    z=logits/temperature; z=z-z.max(); p=np.exp(z); return p/p.sum()
