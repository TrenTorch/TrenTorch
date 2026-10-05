import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    return df.select_dtypes("number").corr()


def heatmap_axes(corr: pd.DataFrame, annotate: bool):
    return sns.heatmap(corr, cmap="coolwarm", vmin=-1, vmax=1, center=0, square=True, annot=annotate, fmt=".2f")


def upper_triangle_mask(n: int) -> np.ndarray:
    return np.triu(np.ones((n, n), dtype=bool), k=1)


def masked_heatmap(corr: pd.DataFrame):
    mask = upper_triangle_mask(len(corr))
    return sns.heatmap(corr, cmap="coolwarm", vmin=-1, vmax=1, center=0, square=True, annot=True, fmt=".2f", mask=mask)
