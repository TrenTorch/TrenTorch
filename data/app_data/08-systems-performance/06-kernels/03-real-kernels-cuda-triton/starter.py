import numpy as np


def compute_grid_size(n_elements: int, threads_per_block: int) -> int:
    """
    A CUDA/Triton kernel launch config has a fixed BLOCK size (how many
    threads run together in one block) and a GRID size (how many
    blocks to launch) -- the grid needs enough blocks that every one of
    n_elements has some thread assigned to it, even when n_elements
    isn't an exact multiple of threads_per_block.

    Returns the number of blocks needed (rounding UP, "ceiling
    division" -- a partially-full last block still needs to be
    launched).
    """
    # TODO: ceiling division of n_elements by threads_per_block.
    # `-(-a // b)` is a common integer trick for ceiling division
    # without importing math.ceil.
    pass


def global_thread_index(block_idx: int, thread_idx: int, threads_per_block: int) -> int:
    """
    Every thread in a real kernel launch knows its own block_idx (which
    block it's in) and thread_idx (its position within that block).
    This is the standard formula every real CUDA/Triton kernel uses to
    turn those two into a single flat index into the actual data array.
    """
    # TODO: block_idx * threads_per_block + thread_idx.
    pass


def simulate_kernel_launch(n_elements: int, threads_per_block: int) -> np.ndarray:
    """
    Simulates launching compute_grid_size(...) blocks of
    threads_per_block threads each, and for every thread whose
    global_thread_index lands within n_elements (some threads in the
    last, partially-full block will land OUTSIDE it -- a real kernel
    always bounds-checks this), marks that position as covered.

    Returns a boolean array of length n_elements: True at every
    position some real thread actually touched.
    """
    # TODO: loop over every (block_idx, thread_idx) pair the launch
    # config implies, compute each one's global_thread_index, and if
    # it's < n_elements, mark `covered[gid] = True`. Every position
    # should end up covered exactly once.
    pass
