
import numpy as np

from _load import load_solution

build_tree = load_solution("decision-trees-best-split-minimal-tree").build_tree
predict_tree = load_solution("decision-trees-best-split-minimal-tree").predict_tree


def adaboost_train(
    input: np.ndarray,
    labels: np.ndarray,
    n_rounds: int,
    max_depth: int = 1,
    seed: int | None = None,
) -> list[tuple[dict, float]]:
    n_samples = input.shape[0]
    weights = np.full(n_samples, 1.0 / n_samples)
    rng = np.random.default_rng(seed)
    ensemble = []

    for _ in range(n_rounds):
        sample_idx = rng.choice(n_samples, size=n_samples, replace=True, p=weights)
        tree = build_tree(input[sample_idx], labels[sample_idx], max_depth)

        predictions = predict_tree(tree, input)
        incorrect = predictions != labels
        weighted_error = np.clip(np.sum(weights[incorrect]), 1e-10, 1 - 1e-10)
        alpha = 0.5 * np.log((1 - weighted_error) / weighted_error)

        weights = weights * np.exp(-alpha * labels * predictions)
        weights = weights / weights.sum()

        ensemble.append((tree, alpha))

    return ensemble


def adaboost_predict(ensemble: list[tuple[dict, float]], input: np.ndarray) -> np.ndarray:
    scores = np.zeros(input.shape[0])
    for tree, alpha in ensemble:
        scores += alpha * predict_tree(tree, input)
    return np.sign(scores).astype(int)
