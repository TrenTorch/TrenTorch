def update_running_stats(running_mean, running_var, batch_mean, batch_var, momentum=0.1):
    """
    running_mean, running_var: current running estimates, shape (D,)
    batch_mean, batch_var: statistics from the current training batch, shape (D,)
    momentum: weight given to the new batch statistics

    Returns:
        (new_running_mean, new_running_var) after one exponential moving average step.
    """
    # TODO: Blend the old running estimates with the batch statistics by momentum.
    pass
