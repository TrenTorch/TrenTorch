import math

def solve(t,T,lr_max,lr_min): return lr_min+0.5*(lr_max-lr_min)*(1+math.cos(math.pi*t/T))
