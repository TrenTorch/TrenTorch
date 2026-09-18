from typing import Callable


def best_epoch_with_min_delta(history: list[float], min_delta: float = 0.0) -> int:
    """
    history: validation losses so far, one per epoch (lower is better).
    min_delta: an improvement only counts if it beats the previous best
    by more than this much.

    Returns:
        the index of the best epoch so far, under that "must beat by
        more than min_delta" rule.
    """
    # TODO: Walk history once, tracking the best value seen and its
    # index, only updating when a later value is smaller than
    # best_value - min_delta (not just smaller).
    pass


def early_stopping_should_stop(history: list[float], patience: int, min_delta: float = 0.0) -> bool:
    """
    Returns:
        True if it's been at least `patience` epochs since the best
        epoch (per best_epoch_with_min_delta), False otherwise
        (including for an empty history).
    """
    # TODO: If history is empty, False. Otherwise compare
    # (len(history)-1) - best_epoch_with_min_delta(...) against patience.
    pass


def train_with_early_stopping(
    step_fn: Callable[[int], tuple[object, float]],
    max_epochs: int,
    patience: int,
    min_delta: float = 0.0,
) -> dict:
    """
    step_fn(epoch) -> (state, val_loss): runs one epoch of training and
    returns whatever "state" means for the caller (e.g. model weights)
    plus that epoch's validation loss.

    Returns a dict:
      "best_state": the state from whichever epoch had the best val_loss
      "best_loss": that val_loss
      "history": every val_loss seen, in order
      "stopped_epoch": the epoch index training actually stopped at
    """
    # TODO: Call step_fn once per epoch (up to max_epochs), appending
    # each val_loss to history. Track best_state/best_loss whenever a
    # NEW epoch beats the previous best by more than min_delta. After
    # each epoch, check early_stopping_should_stop() on the history so
    # far and break out of the loop if it says to stop.
    pass
