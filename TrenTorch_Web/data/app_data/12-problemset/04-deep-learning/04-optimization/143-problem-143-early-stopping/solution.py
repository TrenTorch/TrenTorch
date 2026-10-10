import numpy as np

def solve(losses,patience):
        best=float('inf'); bad=0
        for loss in losses:
            if loss < best: best=loss; bad=0
            else: bad+=1
            if bad>=patience: return True
        return False
