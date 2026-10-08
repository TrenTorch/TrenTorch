import numpy as np


def continuation_logprob(log_probs, tokens, start):
    """
    log_probs: log-probabilities of the next token at each position, shape (T, V);
        row t is the distribution used to predict tokens[t]
    tokens: the full token sequence (prompt followed by continuation)
    start: index of the first continuation token

    Returns:
        The total log-probability of tokens[start:], a float.
    """
    # TODO: Sum the log-probability of each continuation token (see Theory).
    pass
