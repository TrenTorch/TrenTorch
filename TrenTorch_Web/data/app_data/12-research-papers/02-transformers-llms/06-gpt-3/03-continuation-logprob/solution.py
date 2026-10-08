import numpy as np


def continuation_logprob(log_probs, tokens, start):
    return float(sum(log_probs[t, tokens[t]] for t in range(start, len(tokens))))
