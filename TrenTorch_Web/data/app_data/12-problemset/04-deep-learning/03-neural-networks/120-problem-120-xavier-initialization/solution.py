import numpy as np

def solve(fan_in,fan_out,seed=0):
        rng=np.random.default_rng(seed); a=np.sqrt(6/(fan_in+fan_out)); return rng.uniform(-a,a,(fan_in,fan_out))
