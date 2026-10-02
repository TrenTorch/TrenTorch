import numpy as np


def five_number_summary(x: np.ndarray) -> tuple:
    x = np.asarray(x, dtype=float)
    q1, median, q3 = np.percentile(x, [25, 50, 75])
    return float(x.min()), float(q1), float(median), float(q3), float(x.max())


def box_plot_stats(x: np.ndarray, whisker: float = 1.5) -> dict:
    x = np.asarray(x, dtype=float)
    q1, median, q3 = np.percentile(x, [25, 50, 75])
    iqr = q3 - q1
    lower_fence = q1 - whisker * iqr
    upper_fence = q3 + whisker * iqr
    inside = x[(x >= lower_fence) & (x <= upper_fence)]
    outside = np.sort(x[(x < lower_fence) | (x > upper_fence)])
    return {
        "q1": float(q1),
        "median": float(median),
        "q3": float(q3),
        "lower_whisker": float(inside.min()),
        "upper_whisker": float(inside.max()),
        "outliers": outside,
    }
