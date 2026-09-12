import numpy as np


def bootstrap_resample(x: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    return rng.choice(x, size=len(x), replace=True)


def bootstrap_confidence_interval(
    x: np.ndarray,
    statistic_fn,
    n_bootstrap: int = 1000,
    confidence: float = 0.95,
    seed: int | None = None,
) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    bootstrap_statistics = np.empty(n_bootstrap)
    for i in range(n_bootstrap):
        resample = bootstrap_resample(x, rng)
        bootstrap_statistics[i] = statistic_fn(resample)

    lower_percentile = (1.0 - confidence) / 2.0 * 100.0
    upper_percentile = (1.0 + confidence) / 2.0 * 100.0
    return (
        float(np.percentile(bootstrap_statistics, lower_percentile)),
        float(np.percentile(bootstrap_statistics, upper_percentile)),
    )
