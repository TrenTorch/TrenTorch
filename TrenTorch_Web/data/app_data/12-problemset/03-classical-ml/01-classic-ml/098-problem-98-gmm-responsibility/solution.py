import numpy as np

def solve(x,weights,means,covs):
        logs=np.array([np.log(w)+gaussian_logpdf(x,m,c) for w,m,c in zip(weights,means,covs)]); z=np.max(logs); q=np.exp(logs-z); return q/q.sum()
