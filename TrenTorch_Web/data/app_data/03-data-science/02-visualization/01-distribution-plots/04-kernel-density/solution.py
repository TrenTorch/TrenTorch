import numpy as np


def gaussian_kde(x: np.ndarray, grid: np.ndarray, bandwidth: float) -> np.ndarray:
    if bandwidth <= 0:
        raise ValueError("bandwidth must be positive")
    x = np.asarray(x, dtype=float)
    grid = np.asarray(grid, dtype=float)
    scaled = (grid[:, None] - x[None, :]) / bandwidth
    bumps = np.exp(-0.5 * scaled**2) / (bandwidth * np.sqrt(2.0 * np.pi))
    return bumps.mean(axis=1)


def silverman_bandwidth(x: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    q1, q3 = np.percentile(x, [25, 75])
    spreads = [s for s in (x.std(ddof=1), (q3 - q1) / 1.34) if s > 0]
    if not spreads:
        return 1.0
    return float(0.9 * min(spreads) * len(x) ** (-1.0 / 5.0))


def integrate_density(density: np.ndarray, grid: np.ndarray) -> float:
    density = np.asarray(density, dtype=float)
    grid = np.asarray(grid, dtype=float)
    return float(np.sum(np.diff(grid) * (density[:-1] + density[1:]) / 2.0))
