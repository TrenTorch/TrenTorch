def zero_memory_per_gpu(psi, N, stage):
    if stage == 0:
        return 16 * psi
    if stage == 1:
        return 4 * psi + 12 * psi / N
    if stage == 2:
        return 2 * psi + 14 * psi / N
    return 16 * psi / N
