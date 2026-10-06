import numpy as np

def solve(x):
        forbidden=('target','label','future','outcome','post_'); return [c for c in columns if any(k in c.lower() for k in forbidden)]
