import numpy as np


def compute_grid_size(n_elements: int, threads_per_block: int) -> int:
    return -(-n_elements // threads_per_block)


def global_thread_index(block_idx: int, thread_idx: int, threads_per_block: int) -> int:
    return block_idx * threads_per_block + thread_idx


def simulate_kernel_launch(n_elements: int, threads_per_block: int) -> np.ndarray:
    num_blocks = compute_grid_size(n_elements, threads_per_block)
    covered = np.zeros(n_elements, dtype=bool)

    for block_idx in range(num_blocks):
        for thread_idx in range(threads_per_block):
            gid = global_thread_index(block_idx, thread_idx, threads_per_block)
            if gid < n_elements:
                covered[gid] = True

    return covered
