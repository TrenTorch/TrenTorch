import pandas as pd
import plotly.graph_objects as go


def heatmap_figure(z, x_labels, y_labels, title: str, zmin: float, zmax: float, colorscale: str) -> go.Figure:
    fig = go.Figure(
        data=[
            go.Heatmap(
                z=[list(row) for row in z],
                x=list(x_labels),
                y=list(y_labels),
                colorscale=colorscale,
                zmin=zmin,
                zmax=zmax,
                colorbar=dict(title=dict(text="value")),
            )
        ]
    )
    fig.update_layout(title=title)
    return fig


def correlation_heatmap(df: pd.DataFrame) -> go.Figure:
    corr = df.select_dtypes("number").corr()
    fig = heatmap_figure(corr.to_numpy().tolist(), corr.columns.tolist(), corr.index.tolist(), "Correlation", -1, 1, "RdBu")
    fig.update_traces(zmid=0, texttemplate="%{z:.2f}")
    return fig


def annotate_strong_cells(fig: go.Figure, z, x_labels, y_labels, threshold: float) -> int:
    count = 0
    for i, row in enumerate(z):
        for j, value in enumerate(row):
            if abs(value) >= threshold:
                fig.add_annotation(x=x_labels[j], y=y_labels[i], text=f"{value:.2f}", showarrow=False)
                count += 1
    return count
