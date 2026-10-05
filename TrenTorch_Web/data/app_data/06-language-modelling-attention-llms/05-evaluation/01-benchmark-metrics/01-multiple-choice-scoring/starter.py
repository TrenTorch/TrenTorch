import numpy as np


def choice_scores(logprobs, lengths, mode: str = "sum") -> np.ndarray:
    """'sum' returns logprobs, 'mean' returns logprobs / lengths, otherwise ValueError."""
    # TODO
    pass


def pick_choice(logprobs, lengths, mode: str = "sum") -> int:
    """Index of the best-scoring candidate (lowest index on ties)."""
    # TODO
    pass


def multiple_choice_accuracy(all_logprobs, all_lengths, labels, mode: str = "sum") -> float:
    """Fraction of questions whose picked index equals the label."""
    # TODO
    pass
