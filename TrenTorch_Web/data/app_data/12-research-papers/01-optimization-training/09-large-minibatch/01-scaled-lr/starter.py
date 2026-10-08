def scaled_lr(base_lr, batch, base_batch):
    """
    base_lr: learning rate tuned for base_batch
    batch: the new minibatch size; base_batch: the size base_lr was tuned for

    Returns:
        The learning rate scaled linearly with the batch size, base_lr * batch / base_batch.
    """
    # TODO: Scale the base learning rate by the ratio of batch sizes (see Theory).
    pass
