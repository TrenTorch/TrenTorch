import numpy as np

def solve(X,labels,K):
        X=np.asarray(X,float); out=[]
        for k in range(K):
            pts=X[np.asarray(labels)==k]; out.append(pts.mean(0) if len(pts) else np.zeros(X.shape[1]))
        return np.asarray(out)
