import plotly.graph_objects as go
import plotly.io as pio


def line_figure(x, y, name: str, title: str, xlabel: str, ylabel: str) -> go.Figure:
    """
    A new Figure with ONE Scatter trace through (x, y), mode "lines+markers",
    called `name`; layout title `title`, axis titles `xlabel` and `ylabel`.
    """
    # TODO: Build the trace, put it in a figure, set the layout.
    pass


def add_series(fig: go.Figure, x, y, name: str, color: str) -> go.Figure:
    """Add a lines-only Scatter with this name and line colour. Returns the same figure."""
    # TODO: Append one more trace.
    pass


def trace_summaries(fig: go.Figure) -> list:
    """[{"name": ..., "type": ..., "n_points": ...}, ...], one dict per trace, in order."""
    # TODO: Read each trace back.
    pass


def set_axis_ranges(fig: go.Figure, xrange, yrange) -> go.Figure:
    """Fix the visible range of both axes ([low, high] each). Returns the same figure."""
    # TODO: Update both axes.
    pass


def json_roundtrip(fig: go.Figure) -> go.Figure:
    """Serialise `fig` to JSON and rebuild a NEW figure from the text."""
    # TODO: Use plotly.io.
    pass
