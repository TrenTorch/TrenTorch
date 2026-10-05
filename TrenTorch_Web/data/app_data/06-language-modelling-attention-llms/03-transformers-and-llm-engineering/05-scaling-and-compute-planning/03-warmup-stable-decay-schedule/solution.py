def wsd_lr(step, peak_lr, warmup_steps, decay_start, total_steps, final_ratio):
    if step < warmup_steps:
        return peak_lr * (step + 1) / warmup_steps
    if step < decay_start:
        return peak_lr
    span = total_steps - decay_start
    p = 1.0 if span <= 0 else min(max((step - decay_start) / span, 0.0), 1.0)
    return peak_lr * (1.0 - p * (1.0 - final_ratio))
