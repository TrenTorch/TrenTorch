import numpy as np

def solve(X, h0, Wx, Wh, b):
    """An RNN sequence applies the same hidden-state update in order and returns each successive hidden state."""
    X,h,Wx,Wh,b=map(lambda a:np.asarray(a,dtype=float),(X,h0,Wx,Wh,b)); states=[]
    for x in X:
        h=np.tanh(Wx@x+Wh@h+b); states.append(h.copy())
    return np.asarray(states)
