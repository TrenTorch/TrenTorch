import numpy as np


def cpc_loss(scores, pos):
    """
    scores: compatibility scores of the context with N candidate future latents, shape (N,)
    pos: index of the true future latent

    Returns:
        -log softmax(scores)[pos], as a float.
    """
    # TODO: Compute the softmax log-loss of the true candidate (see Theory).
    pass
