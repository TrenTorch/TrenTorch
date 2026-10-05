import plotly.graph_objects as go
import plotly.io as pio


def line_figure(x, y, name: str, title: str, xlabel: str, ylabel: str) -> go.Figure:
    fig = go.Figure(data=[go.Scatter(x=x, y=y, mode="lines+markers", name=name)])
    fig.update_layout(title=title, xaxis_title=xlabel, yaxis_title=ylabel)
    return fig


def add_series(fig: go.Figure, x, y, name: str, color: str) -> go.Figure:
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name=name, line=dict(color=color)))
    return fig


def trace_summaries(fig: go.Figure) -> list:
    return [{"name": trace.name, "type": trace.type, "n_points": len(trace.x)} for trace in fig.data]


def set_axis_ranges(fig: go.Figure, xrange, yrange) -> go.Figure:
    fig.update_xaxes(range=list(xrange))
    fig.update_yaxes(range=list(yrange))
    return fig


def json_roundtrip(fig: go.Figure) -> go.Figure:
    return pio.from_json(pio.to_json(fig))
