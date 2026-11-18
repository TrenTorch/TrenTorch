def scaled_lr(base_lr, batch, base_batch):
    return base_lr * batch / base_batch
