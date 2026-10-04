import numpy as np

def solve(cache,new_value):
        return np.concatenate([cache,new_value[None,...]],axis=-2)
