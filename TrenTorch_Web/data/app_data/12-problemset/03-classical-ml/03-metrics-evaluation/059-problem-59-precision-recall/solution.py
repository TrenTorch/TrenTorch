import numpy as np

def solve(y,pred):
        y,p=np.asarray(y),np.asarray(pred); tp=np.sum((y==1)&(p==1)); fp=np.sum((y==0)&(p==1)); fn=np.sum((y==1)&(p==0)); return (tp/(tp+fp) if tp+fp else 0.0, tp/(tp+fn) if tp+fn else 0.0)
