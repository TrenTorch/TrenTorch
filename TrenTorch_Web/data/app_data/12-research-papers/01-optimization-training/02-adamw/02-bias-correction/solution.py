def bias_corrected(m, v, beta1, beta2, t):
    return m / (1 - beta1**t), v / (1 - beta2**t)
