def xgb_logistic_grad_hess(y, p):
    return p - y, p * (1 - p)
