def bytes_per_param(zero_stage, n_gpus):
    if zero_stage not in (0, 1, 2, 3):
        raise ValueError(f"bad stage: {zero_stage}")
    weights, grads, opt = 2.0, 2.0, 12.0
    if zero_stage >= 1:
        opt /= n_gpus
    if zero_stage >= 2:
        grads /= n_gpus
    if zero_stage >= 3:
        weights /= n_gpus
    return weights + grads + opt


def training_memory_gib(n_params, zero_stage, n_gpus):
    return n_params * bytes_per_param(zero_stage, n_gpus) / 2 ** 30
