import numpy as np

def solve(n):
        i=np.arange(n)[:,None]; j=np.arange(n)[None,:]; return i>=j
