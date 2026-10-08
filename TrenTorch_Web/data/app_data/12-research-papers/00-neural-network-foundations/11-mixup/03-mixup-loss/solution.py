def mixup_loss(loss_a, loss_b, lam):
    return lam * loss_a + (1 - lam) * loss_b
