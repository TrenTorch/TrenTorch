import numpy as np

_EPS = 1e-12


def bce_loss_forward(probs: np.ndarray, target: np.ndarray, reduction: str = "mean"):
    """
    Mirrors torch.nn.functional.binary_cross_entropy(probs, target, reduction=reduction).

    Unlike classification-bce-loss (Classical ML), which takes raw
    sigmoid *logits*, this takes `probs`, already-sigmoided values in
    (0, 1), matching what real torch.nn.functional.binary_cross_entropy
    itself expects (as opposed to *_with_logits, the fused variant
    classification-production-bce-with-logits covers).

        elementwise_i = -(target_i * log(probs_i) + (1 - target_i) * log(1 - probs_i))

    `probs` is clipped to [_EPS, 1 - _EPS] first: log(0) is -inf, and a
    probs value of exactly 0.0 or 1.0 (easy to hit after training pushes
    a sigmoid output to its extreme) would otherwise blow up the loss.
    """
    pass


def bce_loss_backward(
    probs: np.ndarray, target: np.ndarray, reduction: str = "mean", grad_output=1.0
) -> np.ndarray:
    """
    dL/d_probs for BCE (same clipping as forward, for the same reason):

        elementwise_grad_i = (probs_i - target_i) / (probs_i * (1 - probs_i))

    divided by the element count for "mean" (same convention 01-mse
    and 02-cross-entropy both use).
    """
    pass
