import numpy as np

def solve(theta,g,lr,b1,b2,eps):
    theta=np.asarray(theta,float); g=np.asarray(g,float); m=(1-b1)*g; v=(1-b2)*(g*g); mh=m/(1-b1); vh=v/(1-b2); return theta-lr*mh/(np.sqrt(vh)+eps)
