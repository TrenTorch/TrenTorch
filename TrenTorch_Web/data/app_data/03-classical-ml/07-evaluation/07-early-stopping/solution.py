from typing import Callable


def best_epoch_with_min_delta(history: list[float], min_delta: float = 0.0) -> int:
    best_idx = 0
    best_value = history[0]
    for i, value in enumerate(history):
        if value < best_value - min_delta:
            best_value = value
            best_idx = i
    return best_idx


def early_stopping_should_stop(history: list[float], patience: int, min_delta: float = 0.0) -> bool:
    if len(history) == 0:
        return False
    best_idx = best_epoch_with_min_delta(history, min_delta)
    epochs_since_best = (len(history) - 1) - best_idx
    return epochs_since_best >= patience


def train_with_early_stopping(
    step_fn: Callable[[int], tuple[object, float]],
    max_epochs: int,
    patience: int,
    min_delta: float = 0.0,
) -> dict:
    history = []
    best_state, best_loss = None, float("inf")

    for epoch in range(max_epochs):
        state, val_loss = step_fn(epoch)
        history.append(val_loss)

        if val_loss < best_loss - min_delta:
            best_loss = val_loss
            best_state = state

        if early_stopping_should_stop(history, patience, min_delta):
            break

    return {
        "best_state": best_state,
        "best_loss": best_loss,
        "history": history,
        "stopped_epoch": len(history) - 1,
    }
