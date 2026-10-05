import numpy as np


def trigram_next_distribution(sentences: list[list[str]], w1: str, w2: str, alpha: float = 1.0):
    """
    Returns (vocab, probs): the sorted vocabulary (tokens seen plus
    '</s>') and the add-alpha probability of each token following the
    context (w1, w2). Sentences are padded with two '<s>' and one '</s>'.
    """
    # TODO: Count triples, read the counts for (w1, w2), smooth, normalise.
    pass
