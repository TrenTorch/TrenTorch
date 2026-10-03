def detect_loss_spikes(loss_history: list[float], window: int, spike_ratio: float) -> list[int]:
    """
    Flags every step (by index) whose loss is more than `spike_ratio`
    TIMES the average of the preceding `window` steps' losses, an early
    warning sign of training instability (a real gradient explosion or
    bad batch), rather than waiting to see if the run fully diverges.
    """
    pass


def is_diverging(loss_history: list[float], window: int) -> bool:
    """
    `True` if the average loss over the most recent `window` steps is
    HIGHER than the average loss over the `window` steps before that
    (a sustained upward trend, not just one noisy spike). Returns
    `False` if there isn't yet enough history (fewer than `2 * window`
    steps) to compare two full windows.
    """
    pass
