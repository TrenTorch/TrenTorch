import numpy as np

def solve(x,h,c,W,b):
        z=W@np.r_[x,h]+b; i,f,o,g=np.split(z,4); i=1/(1+np.exp(-i)); f=1/(1+np.exp(-f)); o=1/(1+np.exp(-o)); g=np.tanh(g); c=f*c+i*g; return o*np.tanh(c),c
