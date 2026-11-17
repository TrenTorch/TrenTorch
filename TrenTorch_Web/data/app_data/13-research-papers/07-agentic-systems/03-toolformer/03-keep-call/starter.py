def keep_call(loss_without, loss_with, tau):
    """
    loss_without: model loss on the following tokens without the API call
    loss_with: model loss on the following tokens with the API call and its result
    tau: minimum loss reduction required to keep the call

    Returns:
        True if the call reduces the loss by at least tau, so it is kept in the training data.
    """
    # TODO: Compare the loss reduction from the call with the threshold (see Theory).
    pass
