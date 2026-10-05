import numpy as np

def solve(i,f,o,g,c_prev):
    i,f,o,g,c_prev=map(lambda z:np.asarray(z,float),(i,f,o,g,c_prev)); c=f*c_prev+i*g; h=o*np.tanh(c); return h,c
