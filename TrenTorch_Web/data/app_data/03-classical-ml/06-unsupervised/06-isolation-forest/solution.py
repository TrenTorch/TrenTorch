import numpy as np


def _average_path_length_correction(n: int) -> float:
    if n <= 1:
        return 0.0
    return 2.0 * (np.log(n - 1) + 0.5772156649) - 2.0 * (n - 1) / n


def build_isolation_tree(input: np.ndarray, max_depth: int, rng: np.random.Generator) -> dict:
    n_samples, n_features = input.shape
    if max_depth == 0 or n_samples <= 1:
        return {"leaf": True, "size": n_samples}

    feature = rng.integers(0, n_features)
    column = input[:, feature]
    min_value, max_value = column.min(), column.max()
    if min_value == max_value:
        return {"leaf": True, "size": n_samples}

    threshold = rng.uniform(min_value, max_value)
    left_mask = column < threshold
    if left_mask.sum() == 0 or (~left_mask).sum() == 0:
        return {"leaf": True, "size": n_samples}

    return {
        "leaf": False,
        "feature": feature,
        "threshold": threshold,
        "left": build_isolation_tree(input[left_mask], max_depth - 1, rng),
        "right": build_isolation_tree(input[~left_mask], max_depth - 1, rng),
    }


def path_length(tree: dict, x: np.ndarray, current_depth: int = 0) -> float:
    if tree["leaf"]:
        return current_depth + _average_path_length_correction(tree["size"])
    if x[tree["feature"]] < tree["threshold"]:
        return path_length(tree["left"], x, current_depth + 1)
    return path_length(tree["right"], x, current_depth + 1)


def isolation_forest_fit(
    input: np.ndarray, n_trees: int, max_depth: int, seed: int | None = None
) -> list[dict]:
    rng = np.random.default_rng(seed)
    return [build_isolation_tree(input, max_depth, rng) for _ in range(n_trees)]


def anomaly_scores(forest: list[dict], input: np.ndarray, sample_size: int) -> np.ndarray:
    average_path_lengths = np.array(
        [np.mean([path_length(tree, x) for tree in forest]) for x in input]
    )
    normalization = _average_path_length_correction(sample_size)
    return 2.0 ** (-average_path_lengths / normalization)
