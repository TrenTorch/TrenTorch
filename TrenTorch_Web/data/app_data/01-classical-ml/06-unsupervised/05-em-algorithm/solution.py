import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

gaussian_log_likelihood = load_solution(
    "01-classical-ml/05-instance-based-probabilistic/03-gaussian-naive-bayes"
).gaussian_log_likelihood
gmm_e_step = load_solution("01-classical-ml/06-unsupervised/04-gaussian-mixture").gmm_e_step
gmm_m_step = load_solution("01-classical-ml/06-unsupervised/04-gaussian-mixture").gmm_m_step


def gmm_log_likelihood(
    input: np.ndarray, weights: np.ndarray, means: np.ndarray, variances: np.ndarray
) -> float:
    n_samples = input.shape[0]
    n_components = weights.shape[0]

    log_probs = np.empty((n_samples, n_components))
    for j in range(n_components):
        for i in range(n_samples):
            log_probs[i, j] = np.log(weights[j]) + gaussian_log_likelihood(
                input[i], means[j], variances[j]
            )

    max_log = log_probs.max(axis=1, keepdims=True)
    per_sample = max_log[:, 0] + np.log(np.sum(np.exp(log_probs - max_log), axis=1))
    return float(np.sum(per_sample))


def fit_gmm(input: np.ndarray, n_components: int, max_iter: int, seed: int | None = None) -> dict:
    rng = np.random.default_rng(seed)
    n_samples = input.shape[0]

    init_idx = rng.choice(n_samples, n_components, replace=False)
    means = input[init_idx].copy()
    weights = np.full(n_components, 1.0 / n_components)
    variances = np.tile(input.var(axis=0), (n_components, 1))

    log_likelihood_history = []
    responsibilities = None
    for _ in range(max_iter):
        responsibilities = gmm_e_step(input, weights, means, variances)
        weights, means, variances = gmm_m_step(input, responsibilities)
        log_likelihood_history.append(gmm_log_likelihood(input, weights, means, variances))

    return {
        "weights": weights,
        "means": means,
        "variances": variances,
        "responsibilities": responsibilities,
        "log_likelihood_history": np.array(log_likelihood_history),
    }
