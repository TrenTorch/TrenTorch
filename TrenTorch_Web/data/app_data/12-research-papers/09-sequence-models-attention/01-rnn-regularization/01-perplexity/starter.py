import math


def perplexity(total_nll, n):
    """
    total_nll: summed negative log-likelihood of n tokens (nats)
    n: number of tokens scored

    Returns:
        The perplexity exp(total_nll / n), the standard language-model metric.
    """
    # TODO: Exponentiate the average per-token negative log-likelihood (see Theory).
    pass
