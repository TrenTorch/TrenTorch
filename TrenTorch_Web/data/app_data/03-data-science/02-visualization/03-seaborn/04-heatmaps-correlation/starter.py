import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Pearson correlations of the numeric columns (names as index and columns)."""
    # TODO: Select the numeric columns and correlate them.
    pass


def heatmap_axes(corr: pd.DataFrame, annotate: bool):
    """
    sns.heatmap of `corr`: cmap "coolwarm", scale fixed to -1..1 centred at 0,
    square cells, values with 2 decimals if `annotate`. Returns the Axes.
    """
    # TODO: Draw the heatmap with a pinned colour scale.
    pass


def upper_triangle_mask(n: int) -> np.ndarray:
    """n x n boolean array, True strictly above the diagonal."""
    # TODO: Build the triangle.
    pass


def masked_heatmap(corr: pd.DataFrame):
    """Annotated heatmap with the cells above the diagonal hidden. Returns the Axes."""
    # TODO: Same heatmap plus the mask.
    pass
