import numpy as np


def prepare_batch(
    flat_data: np.ndarray, batch_size: int, feature_count: int, num_groups: int
) -> dict:
    batch = flat_data.reshape(batch_size, feature_count)
    transposed = batch.T
    with_channel = transposed[np.newaxis, :, :]
    groups = np.split(with_channel, num_groups, axis=1)

    return {
        "batch": batch,
        "transposed": transposed,
        "with_channel": with_channel,
        "groups": groups,
        "with_channel_shares_memory_with_flat_data": bool(
            np.shares_memory(with_channel, flat_data)
        ),
        "groups_first_shares_memory_with_flat_data": bool(
            np.shares_memory(groups[0], flat_data)
        ),
    }
