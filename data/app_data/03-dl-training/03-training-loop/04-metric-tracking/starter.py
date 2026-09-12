import numpy as np


class MetricTracker:
    """
    Records a metric (like loss or accuracy) once per training step or
    epoch, under a name, and can answer three questions about the
    history it's collected: the raw history, a smoothed moving average
    (loss curves are notoriously noisy step-to-step, so this is what a
    loss curve plot usually actually shows), and the best value seen so
    far (for deciding when to save a checkpoint, or for
    `Early stopping: monitor validation loss, restore the best
    checkpoint`, later in this Part).
    """

    def __init__(self):
        self.history: dict[str, list[float]] = {}

    def record(self, name: str, value: float) -> None:
        """Appends `value` to the history list for `name` (creating it if
        this is the first time `name` has been recorded)."""
        pass

    def get_history(self, name: str) -> list[float]:
        """Returns the full recorded history for `name`, or an empty list
        if `name` has never been recorded."""
        pass

    def moving_average(self, name: str, window: int) -> list[float]:
        """
        Returns a list the SAME LENGTH as the recorded history for `name`,
        where entry `i` is the average of the last `window` values UP TO
        AND INCLUDING index `i` (using fewer than `window` values for the
        first few entries, where a full window isn't available yet).
        """
        pass

    def best(self, name: str, mode: str = "min") -> float | None:
        """
        Returns the best value recorded for `name`: the minimum if
        mode="min", the maximum if mode="max". Returns None if `name` has
        never been recorded.
        """
        pass
