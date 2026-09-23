import numpy as np


def bootstrap_sample_with_oob(
    input: np.ndarray, targets: np.ndarray, seed: int | None = None
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Like 02-bagging's bootstrap_sample, plus also returns which row
    indices were never drawn (the "out-of-bag" samples for this
    particular bootstrap draw).

    Returns:
        boot_input, boot_targets: the resampled data, same as before.
        oob_indices: sorted array of indices into the ORIGINAL input
        that never appeared in this bootstrap draw.
    """
    # TODO: Draw the resampled indices the same way bootstrap_sample
    # does. Then figure out which of the original 0..n_samples-1
    # indices never appeared in that draw (np.where on a boolean
    # "was this index drawn" array works well here).
    pass


def train_random_forest_regressor(
    input: np.ndarray,
    targets: np.ndarray,
    n_trees: int,
    max_depth: int,
    seed: int | None = None,
) -> list[tuple[dict, np.ndarray]]:
    """
    Returns a list of (tree, oob_indices) pairs, one per tree, each
    tree trained via build_regression_tree on its own bootstrap sample.
    """
    # TODO: One rng, built once, before the loop. For each of n_trees:
    # bootstrap_sample_with_oob(), build_regression_tree() on the
    # resampled data, collect (tree, oob_indices).
    pass


def predict_random_forest_regressor(
    forest: list[tuple[dict, np.ndarray]], input: np.ndarray
) -> np.ndarray:
    """Averages every tree's prediction (regression: mean, not a vote)."""
    # TODO: predict_regression_tree() with every tree in the forest,
    # then average across trees for each sample.
    pass


def oob_error(forest: list[tuple[dict, np.ndarray]], input: np.ndarray, targets: np.ndarray) -> float:
    """
    For each training sample, averages predictions from only the trees
    that never saw it during training (its out-of-bag trees), then
    returns the mean squared error of those OOB predictions against
    targets. A sample that was in-bag for every tree contributes
    nothing (there's no OOB prediction to make for it).
    """
    # TODO: For each (tree, oob_indices) pair, add that tree's
    # predictions on input[oob_indices] into a running per-sample sum,
    # and increment a per-sample count. Average sum/count for samples
    # with count > 0, then compute MSE against targets for those samples.
    pass
