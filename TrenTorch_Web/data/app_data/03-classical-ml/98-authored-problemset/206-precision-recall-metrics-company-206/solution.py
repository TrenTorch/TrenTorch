import numpy as np

def solve(y_true,y_pred):
    y_true=np.asarray(y_true); y_pred=np.asarray(y_pred)
    tp=np.sum((y_true==1)&(y_pred==1)); fp=np.sum((y_true==0)&(y_pred==1)); fn=np.sum((y_true==1)&(y_pred==0))
    precision=tp/(tp+fp) if tp+fp else 0.0
    recall=tp/(tp+fn) if tp+fn else 0.0
    return float(precision),float(recall)
