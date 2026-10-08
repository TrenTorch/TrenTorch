def adam_update_moments(m, v, grad, beta1=0.9, beta2=0.999):
    new_m = beta1 * m + (1 - beta1) * grad
    new_v = beta2 * v + (1 - beta2) * grad**2
    return new_m, new_v
