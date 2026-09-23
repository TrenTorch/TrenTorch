import numpy as np


def flash_attention(
    query: np.ndarray,
    key: np.ndarray,
    value: np.ndarray,
    block_size: int,
    mask: np.ndarray | None = None,
) -> np.ndarray:
    d_k = query.shape[-1]
    seq_len_k = key.shape[-2]

    running_max = np.full(query.shape[:-1] + (1,), -np.inf)
    running_sum = np.zeros(query.shape[:-1] + (1,))
    running_output = np.zeros(query.shape[:-1] + (value.shape[-1],))

    for start in range(0, seq_len_k, block_size):
        end = min(start + block_size, seq_len_k)
        key_block = key[..., start:end, :]
        value_block = value[..., start:end, :]

        scores = query @ np.swapaxes(key_block, -2, -1) / np.sqrt(d_k)
        if mask is not None:
            scores = scores + mask[..., :, start:end]

        block_max = np.max(scores, axis=-1, keepdims=True)
        new_max = np.maximum(running_max, block_max)

        correction = np.exp(running_max - new_max)
        probs = np.exp(scores - new_max)

        running_sum = correction * running_sum + np.sum(probs, axis=-1, keepdims=True)
        running_output = correction * running_output + probs @ value_block
        running_max = new_max

    return running_output / running_sum
