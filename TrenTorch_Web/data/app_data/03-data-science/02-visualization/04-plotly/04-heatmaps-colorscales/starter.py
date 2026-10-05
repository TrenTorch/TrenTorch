import pandas as pd
import plotly.graph_objects as go


def heatmap_figure(z, x_labels, y_labels, title: str, zmin: float, zmax: float, colorscale: str) -> go.Figure:
    """
    One Heatmap trace: matrix z (list of rows), x/y labels, colour scale and
    range zmin..zmax, colourbar titled "value"; layout title `title`.
    """
    # TODO: Build the heatmap with an explicit colour range.
    pass


def correlation_heatmap(df: pd.DataFrame) -> go.Figure:
    """
    Heatmap of the Pearson correlation matrix of the numeric columns: "RdBu",
    range -1..1 centred at 0, cells labelled with texttemplate "%{z:.2f}".
    """
    # TODO: Correlate, then reuse the heatmap with a pinned, centred scale.
    pass


def annotate_strong_cells(fig: go.Figure, z, x_labels, y_labels, threshold: float) -> int:
    """
    Add a text annotation (value to 2 decimals, showarrow=False) at every cell
    with |value| >= threshold. Returns how many were added.
    """
    # TODO: Loop over the cells and annotate the strong ones.
    pass
