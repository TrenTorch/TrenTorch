import numpy as np


def _log_softmax(logits: np.ndarray) -> np.ndarray:
    shifted = logits - np.max(logits, axis=-1, keepdims=True)
    return shifted - np.log(np.sum(np.exp(shifted), axis=-1, keepdims=True))


def cross_entropy_forward(logits: np.ndarray, target: np.ndarray, reduction: str = "mean"):
    """
    Mirrors torch.nn.functional.cross_entropy(logits, target, reduction=reduction).

    logits: (n, num_classes) raw scores, NOT probabilities.
    target: (n,) integer class indices (0..num_classes-1), NOT one-hot.

    Internally fuses log_softmax with negative log-likelihood:

        log_probs = log_softmax(logits)          # 04-softmax's cousin
        loss_i    = -log_probs[i, target[i]]     # "surprise" at the true class

    `_log_softmax` (the numerically stable log(softmax(x)), computed
    directly rather than as log(softmax(x)) to avoid a redundant
    exp-then-log round trip) is already provided above.

    reduction: "mean" (default), "sum", or "none" (per-example losses).
    """
    pass


def cross_entropy_backward(
    logits: np.ndarray, target: np.ndarray, reduction: str = "mean", grad_output=1.0
) -> np.ndarray:
    """
    The famously clean gradient of softmax + cross-entropy combined:

        dL/d_logits = softmax(logits) - one_hot(target)

    (divided by n for "mean", matching the forward pass's own
    division). This is why real frameworks fuse softmax and
    cross-entropy into one op instead of composing 04-softmax's
    backward with a separate NLL backward, the combined gradient is
    this simple, while going through two separate backward passes
    would be both slower and less numerically stable.
    """
    pass
