import numpy as np


def bootstrap_sample(
    input: np.ndarray, labels: np.ndarray, seed: int | None = None
) -> tuple[np.ndarray, np.ndarray]:
    """
    Draws n_samples indices with replacement (n_samples == input.shape[0])
    and returns the resampled (input, labels), same shapes as the originals.
    """
    # TODO: rng.integers(0, n_samples, size=n_samples) for the resampled
    # indices, then index both input and labels with them.
    pass


def train_random_forest(
    input: np.ndarray,
    labels: np.ndarray,
    n_trees: int,
    max_depth: int,
    seed: int | None = None,
) -> list[dict]:
    """
    Trains n_trees independent trees, each on its own bootstrap sample
    of (input, labels), using build_tree() from
    03-best-split-minimal-tree. The result is directly usable by
    01-random-forest-majority-vote's random_forest_predict.
    """
    # TODO: Build ONE np.random.default_rng(seed), before the loop, not
    # inside it (same reasoning as Linear Regression's mini-batch
    # training question: re-seeding every iteration would give every
    # tree the identical bootstrap sample). For each of n_trees:
    # bootstrap_sample the data, build_tree() on it, collect the trees.
    pass
