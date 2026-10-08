def xgb_split_gain(GL, HL, GR, HR, lam, gamma):
    G = GL + GR
    H = HL + HR
    return 0.5 * (GL**2 / (HL + lam) + GR**2 / (HR + lam) - G**2 / (H + lam)) - gamma
