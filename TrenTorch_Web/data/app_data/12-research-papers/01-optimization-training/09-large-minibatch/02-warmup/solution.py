def gradual_warmup_lr(target, t, warmup):
    return target * min(1.0, t / warmup)
