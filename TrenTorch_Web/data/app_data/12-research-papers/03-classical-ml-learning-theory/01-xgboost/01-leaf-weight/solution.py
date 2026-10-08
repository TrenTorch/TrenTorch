def xgb_leaf_weight(G, H, lam):
    return -G / (H + lam)
