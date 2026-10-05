import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def animated_scatter(df: pd.DataFrame, x: str, y: str, frame: str):
    return px.scatter(
        df,
        x=x,
        y=y,
        animation_frame=frame,
        range_x=[df[x].min(), df[x].max()],
        range_y=[df[y].min(), df[y].max()],
    )


def figure_from_frames(frames: dict) -> go.Figure:
    names = list(frames)
    first_x, first_y = frames[names[0]]
    fig = go.Figure(
        data=[go.Scatter(x=first_x, y=first_y, mode="markers")],
        frames=[go.Frame(data=[go.Scatter(x=x, y=y, mode="markers")], name=name) for name, (x, y) in frames.items()],
    )
    steps = [
        dict(method="animate", label=name, args=[[name], dict(mode="immediate", frame=dict(duration=200, redraw=True))])
        for name in names
    ]
    fig.update_layout(sliders=[dict(steps=steps)])
    return fig


def last_frame_summary(fig: go.Figure) -> dict:
    last = fig.frames[-1]
    xs = list(last.data[0].x)
    return {"name": last.name, "n_points": len(xs), "x_max": float(max(xs))}
