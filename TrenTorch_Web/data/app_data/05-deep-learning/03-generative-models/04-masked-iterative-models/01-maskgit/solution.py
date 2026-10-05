import numpy as np


def maskgit_loss(logits, targets, mask):
    """Compute MaskGIT loss.

    Args:
        logits: Model logits, shape (N, L, V).
        targets: Target token indices, shape (N, L).
        mask: Binary mask (1 for positions to predict), shape (N, L).

    Returns:
        Scalar loss.
    """
    n, l, v = logits.shape
    eps = 1e-7

    log_probs = logits - np.max(logits, axis=2, keepdims=True)
    log_probs = log_probs - np.log(np.sum(np.exp(log_probs), axis=2, keepdims=True) + eps)

    target_log_probs = np.take_along_axis(log_probs, targets[:, :, np.newaxis], axis=2)[:, :, 0]

    ce_loss = -target_log_probs
    masked_loss = ce_loss * mask

    num_masked = np.sum(mask) + eps
    return np.sum(masked_loss) / num_masked
