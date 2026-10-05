import numpy as np

def solve(x, h, Wx, Wh, b):
    """One vanilla RNN step computes h_next=tanh(Wx*x+Wh*h+b)."""
    x,h,Wx,Wh,b=map(np.asarray,(x,h,Wx,Wh,b)); return np.tanh(Wx@x+Wh@h+b)
