import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

gaussian_log_likelihood = load_solution(
    "01-classical-ml/05-instance-based-probabilistic/03-gaussian-naive-bayes"
).gaussian_log_likelihood


def gmm_e_step(
    input: np.ndarray, weights: np.ndarray, means: np.ndarray, variances: np.ndarray
) -> np.ndarray:
    n_samples = input.shape[0]
    n_components = weights.shape[0]

    log_responsibilities = np.empty((n_samples, n_components))
    for j in range(n_components):
        for i in range(n_samples):
            log_responsibilities[i, j] = np.log(weights[j]) + gaussian_log_likelihood(
                input[i], means[j], variances[j]
            )

    max_log = log_responsibilities.max(axis=1, keepdims=True)
    unnormalized = np.exp(log_responsibilities - max_log)
    return unnormalized / unnormalized.sum(axis=1, keepdims=True)


def gmm_m_step(
    input: np.ndarray, responsibilities: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    n_samples, n_components = responsibilities.shape
    effective_counts = responsibilities.sum(axis=0)

    weights = effective_counts / n_samples
    means = (responsibilities.T @ input) / effective_counts[:, np.newaxis]

    variances = np.empty((n_components, input.shape[1]))
    for j in range(n_components):
        diff = input - means[j]
        variances[j] = (responsibilities[:, j] @ (diff**2)) / effective_counts[j]

    return weights, means, variances
