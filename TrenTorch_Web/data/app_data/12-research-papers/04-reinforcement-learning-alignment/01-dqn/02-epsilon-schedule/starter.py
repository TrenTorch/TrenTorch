def epsilon_schedule(step, start, end, decay_steps):
    """
    step: current environment step (non-negative)
    start: exploration rate at step 0
    end: exploration rate after decay_steps
    decay_steps: number of steps over which to decay linearly

    Returns:
        The linearly annealed exploration rate for this step.
    """
    # TODO: Interpolate linearly from start to end over decay_steps, then hold end (see Theory).
    pass
