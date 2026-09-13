"""
pytest data/app_data/08-systems-performance/06-kernels/03-real-kernels-cuda-triton/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"08-systems-performance/06-kernels/{Path(__file__).resolve().parent.name}")
compute_grid_size = _module.compute_grid_size
global_thread_index = _module.global_thread_index
simulate_kernel_launch = _module.simulate_kernel_launch


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_grid_size_matches_hand_computation_for_an_exact_multiple():
    assert compute_grid_size(n_elements=1024, threads_per_block=256) == 4


def test_02_grid_size_rounds_up_for_a_non_exact_multiple():
    assert compute_grid_size(n_elements=1000, threads_per_block=256) == 4  # ceil(1000/256) = 4


# --- Shape / general-case coverage -----------------------------------


def test_03_global_thread_index_matches_hand_computation():
    assert global_thread_index(block_idx=2, thread_idx=5, threads_per_block=256) == 517


def test_04_every_element_is_covered_exactly_once():
    n_elements = 1000
    covered = simulate_kernel_launch(n_elements, threads_per_block=256)
    assert covered.shape == (n_elements,)
    assert np.all(covered)


# --- Parameter handling -------------------------------------------------


def test_05_exact_multiple_of_block_size_needs_no_bounds_checking_waste():
    covered = simulate_kernel_launch(1024, threads_per_block=256)
    assert np.all(covered)
    assert covered.shape == (1024,)


def test_06_grid_size_of_one_block_when_n_elements_fits_in_a_single_block():
    assert compute_grid_size(n_elements=100, threads_per_block=256) == 1
    covered = simulate_kernel_launch(100, threads_per_block=256)
    assert np.all(covered)


# --- Edge cases ---------------------------------------------------------


def test_07_single_element_launch():
    assert compute_grid_size(1, threads_per_block=256) == 1
    covered = simulate_kernel_launch(1, threads_per_block=256)
    assert covered.shape == (1,)
    assert covered[0]


def test_08_threads_per_block_of_one_needs_exactly_n_elements_blocks():
    assert compute_grid_size(n_elements=10, threads_per_block=1) == 10
    covered = simulate_kernel_launch(10, threads_per_block=1)
    assert np.all(covered)


# --- Array hygiene / determinism -----------------------------------------


def test_09_no_thread_ever_writes_outside_the_valid_range():
    # A mutant that skips the gid < n_elements bounds check would crash
    # with an out-of-bounds index the moment n_elements isn't an exact
    # multiple of threads_per_block -- this case deliberately isn't one.
    n_elements = 777
    covered = simulate_kernel_launch(n_elements, threads_per_block=256)
    assert covered.shape == (n_elements,)  # would have raised IndexError otherwise
    assert np.all(covered)


# --- Independent correctness oracle -----------------------------------


def test_10_matches_the_standard_cuda_1d_grid_stride_indexing_pattern():
    # This is the textbook 1D CUDA/Triton kernel launch pattern used in
    # NVIDIA's own official CUDA C++ Programming Guide and in Triton's
    # own tutorials: grid_size = ceil(n / block_size); each thread's
    # global index is blockIdx.x * blockDim.x + threadIdx.x; a
    # bounds check (if (gid < n)) guards the last, partially-full block.
    # Not a fabricated scheme -- the literal standard.
    n_elements, threads_per_block = 2050, 512
    grid_size = compute_grid_size(n_elements, threads_per_block)
    assert grid_size == 5  # ceil(2050/512) = 5, last block only half-full

    covered = simulate_kernel_launch(n_elements, threads_per_block)
    assert covered.shape == (n_elements,)
    assert np.all(covered)

    # the very last valid index should be reachable from the last block
    last_block = grid_size - 1
    last_thread_in_block = (n_elements - 1) - global_thread_index(last_block, 0, threads_per_block)
    assert global_thread_index(last_block, last_thread_in_block, threads_per_block) == n_elements - 1
