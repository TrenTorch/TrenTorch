import numpy as np


def behavioral_cloning_loss(policy_logits, expert_actions):
    """
    Behavioral cloning loss.

    Args:
        policy_logits: predicted action logits (batch_size, num_actions)
        expert_actions: expert action indices (batch_size,)

    Returns:
        loss: scalar cross-entropy loss
    """
    policy_logits = np.array(policy_logits, dtype=np.float32)
    expert_actions = np.array(expert_actions, dtype=np.int32)

    batch_size = policy_logits.shape[0]

    # Numerically stable cross-entropy: LogSoftmax + NLLLoss
    # log_softmax: log(exp(z_i) / sum_j exp(z_j))
    max_logits = np.max(policy_logits, axis=1, keepdims=True)
    log_softmax = policy_logits - max_logits - np.log(
        np.sum(np.exp(policy_logits - max_logits), axis=1, keepdims=True)
    )

    # NLLLoss: -mean(log_softmax[expert_action])
    loss = -np.mean(log_softmax[np.arange(batch_size), expert_actions])

    return float(loss)
