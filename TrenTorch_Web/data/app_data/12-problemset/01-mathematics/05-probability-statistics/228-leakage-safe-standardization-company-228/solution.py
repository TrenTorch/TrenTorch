import numpy as np

def solve(train,val):
    train=np.asarray(train,float); val=np.asarray(val,float); mu=train.mean(axis=0); s=train.std(axis=0); s=np.where(s==0,1,s); return (train-mu)/s,(val-mu)/s
