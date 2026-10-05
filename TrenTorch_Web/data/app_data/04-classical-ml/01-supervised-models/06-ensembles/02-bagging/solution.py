
import numpy as np

from _load import load_solution

build_tree = load_solution("decision-trees-best-split-minimal-tree").build_tree


def bootstrap_sample(
    input: np.ndarray, labels: np.ndarray, seed: int | None = None
) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    n_samples = input.shape[0]
    indices = rng.integers(0, n_samples, size=n_samples)
    return input[indices], labels[indices]


def train_random_forest(
    input: np.ndarray,
    labels: np.ndarray,
    n_trees: int,
    max_depth: int,
    seed: int | None = None,
) -> list[dict]:
    rng = np.random.default_rng(seed)
    trees = []
    for _ in range(n_trees):
        boot_input, boot_labels = bootstrap_sample(input, labels, seed=rng)
        trees.append(build_tree(boot_input, boot_labels, max_depth))
    return trees
