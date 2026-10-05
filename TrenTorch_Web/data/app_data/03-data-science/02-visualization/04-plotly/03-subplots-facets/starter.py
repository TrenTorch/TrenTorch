import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def stacked_panels(x, y_top, y_bottom, titles) -> go.Figure:
    """
    2 rows x 1 column via make_subplots, sharing the x axis, with `titles` as
    subplot titles; a Scatter of (x, y_top) in row 1 and of (x, y_bottom) in row 2.
    """
    # TODO: Make the grid, then add one trace per row.
    pass


def facet_scatter(df, x: str, y: str, col: str, col_order: list):
    """Express scatter with one panel per value of `col`, in `col_order`, left to right."""
    # TODO: Facet by column with a fixed order.
    pass


def panel_titles(fig: go.Figure) -> list:
    """Texts of the subplot/facet titles, in the order of the figure's annotations."""
    # TODO: Read the annotations.
    pass
