import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def animated_scatter(df: pd.DataFrame, x: str, y: str, frame: str):
    """
    Express scatter animated over `frame`, with the axes fixed to the range of
    the WHOLE data: x in [min(x), max(x)], y in [min(y), max(y)].
    """
    # TODO: Animate with fixed ranges.
    pass


def figure_from_frames(frames: dict) -> go.Figure:
    """
    From {name: (x, y)}: initial trace = first entry (markers only); one
    go.Frame per entry (same name); a slider with one step per frame, each
    method="animate", label=name, args[0]=[name].
    """
    # TODO: Build the figure, its frames and the slider by hand.
    pass


def last_frame_summary(fig: go.Figure) -> dict:
    """{"name": ..., "n_points": ..., "x_max": ...} for the last frame's first trace."""
    # TODO: Read the last frame back.
    pass
