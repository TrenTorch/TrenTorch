import numpy as np

def solve(x,y):
    x=np.asarray(x,float); y=np.asarray(y,int); o=np.argsort(x); x=x[o]; y=y[o]; best=(np.inf,None)
    for i in range(1,len(x)):
        if x[i]==x[i-1]: continue
        a,b=y[:i],y[i:]
        def g(z):
            p=np.mean(z==1); return 2*p*(1-p)
        score=(len(a)*g(a)+len(b)*g(b))/len(y); t=(x[i-1]+x[i])/2
        if score<best[0]-1e-12: best=(score,t)
    return best[1]
