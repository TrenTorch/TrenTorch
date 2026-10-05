import numpy as np


def choice_scores(logprobs, lengths, mode="sum"):
    lp = np.asarray(logprobs, dtype=float)
    if mode == "sum":
        return lp
    if mode == "mean":
        return lp / np.asarray(lengths, dtype=float)
    raise ValueError(f"unknown mode: {mode}")


def pick_choice(logprobs, lengths, mode="sum"):
    return int(np.argmax(choice_scores(logprobs, lengths, mode)))


def multiple_choice_accuracy(all_logprobs, all_lengths, labels, mode="sum"):
    hits = [pick_choice(lp, ln, mode) == y for lp, ln, y in zip(all_logprobs, all_lengths, labels)]
    return float(np.mean(hits))
