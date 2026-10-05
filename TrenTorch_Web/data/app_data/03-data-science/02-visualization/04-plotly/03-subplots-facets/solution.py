import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def stacked_panels(x, y_top, y_bottom, titles) -> go.Figure:
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=list(titles))
    fig.add_trace(go.Scatter(x=x, y=y_top), row=1, col=1)
    fig.add_trace(go.Scatter(x=x, y=y_bottom), row=2, col=1)
    return fig


def facet_scatter(df, x: str, y: str, col: str, col_order: list):
    return px.scatter(df, x=x, y=y, facet_col=col, category_orders={col: list(col_order)})


def panel_titles(fig: go.Figure) -> list:
    return [annotation.text for annotation in fig.layout.annotations]
