def effective_decay(lr, wd, steps):
    return (1 - lr * wd) ** steps
