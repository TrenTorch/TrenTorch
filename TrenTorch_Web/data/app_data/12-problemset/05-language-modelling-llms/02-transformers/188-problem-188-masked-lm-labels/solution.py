import numpy as np

def solve(ids,mask,ignore_index=-100):
        ids=np.asarray(ids).copy(); labels=np.full_like(ids,ignore_index); labels[mask]=ids[mask]; return ids,labels
