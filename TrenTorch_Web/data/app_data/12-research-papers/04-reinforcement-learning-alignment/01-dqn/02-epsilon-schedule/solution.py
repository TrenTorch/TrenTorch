def epsilon_schedule(step, start, end, decay_steps):
    if step >= decay_steps:
        return end
    return start + (end - start) * step / decay_steps
