import numpy as np

def solve(x, keep_prob, seed=0):
    """Inverted dropout samples a Bernoulli keep mask and scales retained activations by 1/keep_prob so the expected activation is unchanged."""
    x=np.asarray(x); keep_prob=float(keep_prob)
    if not 0<keep_prob<=1: raise ValueError("keep_prob must be in (0, 1]")
    rng=np.random.default_rng(seed); mask=rng.random(x.shape)<keep_prob; return x*mask/keep_prob
