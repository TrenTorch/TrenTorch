import numpy as np

def solve(y,scores):
    y=np.asarray(y); scores=np.asarray(scores,float); best=(-np.inf,np.inf)
    for t in np.unique(scores):
        p=scores>=t; tp=((y==1)&p).sum(); fn=((y==1)&~p).sum(); fp=((y==0)&p).sum(); tn=((y==0)&~p).sum()
        tpr=tp/(tp+fn) if tp+fn else 0; fpr=fp/(fp+tn) if fp+tn else 0; j=tpr-fpr
        cand=(j,-t)
        if cand>best: best=cand
    return -best[1]
