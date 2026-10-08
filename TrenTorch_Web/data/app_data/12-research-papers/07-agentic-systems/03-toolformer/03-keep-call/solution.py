def keep_call(loss_without, loss_with, tau):
    return (loss_without - loss_with) >= tau
