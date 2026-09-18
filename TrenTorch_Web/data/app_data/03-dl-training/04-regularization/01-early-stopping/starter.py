class EarlyStopping:
    """
    Call `.step(val_loss, state)` once per epoch, right after computing
    that epoch's validation loss. Tracks the BEST validation loss seen so
    far (and, alongside it, whatever `state` was passed in on that best
    epoch, typically a snapshot of the model's weights), and flags
    `should_stop = True` once validation loss has failed to improve for
    `patience` consecutive epochs in a row.
    """

    def __init__(self, patience: int = 5, min_delta: float = 0.0):
        self.patience = patience
        self.min_delta = min_delta
        self.best_loss: float | None = None
        self.best_state = None
        self.counter = 0
        self.should_stop = False

    def step(self, val_loss: float, state=None) -> bool:
        """
        Updates internal tracking with this epoch's val_loss (and state).
        Returns the current value of self.should_stop, so a training loop
        can do `if early_stopping.step(val_loss, model_state): break`.
        """
        pass
