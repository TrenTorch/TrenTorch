def combined_loss(hard_ce, soft_ce, alpha):
    return alpha * soft_ce + (1 - alpha) * hard_ce
