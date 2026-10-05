import numpy as np

def solve(x,y):
    x=np.asarray(x,float); y=np.asarray(y,int)
    order=np.argsort(x); x=x[order]; y=y[order]
    best=None
    for i in range(1,len(x)):
        if x[i]==x[i-1]: continue
        t=(x[i]+x[i-1])/2
        left=y[:i]; right=y[i:]
        def g(a):
            p=np.mean(a==1); return 1-p*p-(1-p)*(1-p)
        s=(len(left)*g(left)+len(right)*g(right))/len(y)
        cand=(s,t)
        if best is None or cand<best: best=cand
    return best[1]
