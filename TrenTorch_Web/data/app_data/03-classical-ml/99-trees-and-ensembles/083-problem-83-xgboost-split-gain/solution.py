import numpy as np

def solve(GL, HL, GR, HR, GP, HP, lam):
    """Implement xgboost split gain according to the contract."""

    def score(g, h):
        return g * g / (h + lam)
    return 0.5 * (score(GL, HL) + score(GR, HR) - score(GP, HP))
