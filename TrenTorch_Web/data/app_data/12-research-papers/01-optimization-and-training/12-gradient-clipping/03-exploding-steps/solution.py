def exploding_steps(grad_norms, threshold):
    return sum(1 for n in grad_norms if n > threshold)
