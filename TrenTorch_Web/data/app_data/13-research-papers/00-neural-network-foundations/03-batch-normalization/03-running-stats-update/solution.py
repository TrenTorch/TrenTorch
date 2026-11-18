def update_running_stats(running_mean, running_var, batch_mean, batch_var, momentum=0.1):
    new_mean = (1 - momentum) * running_mean + momentum * batch_mean
    new_var = (1 - momentum) * running_var + momentum * batch_var
    return new_mean, new_var
