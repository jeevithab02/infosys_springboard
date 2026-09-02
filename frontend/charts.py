"""
Shared, professionally-styled Plotly chart builders.

Centralizing chart styling here keeps every page (dashboard, alerts,
failures, maintenance, analytics) using one consistent, non-default
visual language instead of Streamlit's default chart styling.
"""

import plotly.graph_objects as go

NAVY = "#102532"
MUTED = "#5d7685"
GREEN = "#20c563"
GREEN_DARK = "#16a653"
BLUE = "#3b82e5"
ORANGE = "#e5a13b"
RED = "#e5484d"
GRID = "#eef2f1"

FONT = dict(family="Helvetica, Arial, sans-serif", color=MUTED, size=13)


def _base_layout(height=280, show_legend=False):
    return dict(
        height=height,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=FONT,
        showlegend=show_legend,
        legend=dict(orientation="h", y=-0.15, font=dict(color=MUTED, size=12)),
    )


def area_line_chart(x_values, y_values, name="Value", color=GREEN):
    """A clean gradient area/line chart, e.g. for telemetry trends."""

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=y_values,
            mode="lines",
            name=name,
            line=dict(color=color, width=3, shape="spline", smoothing=0.6),
            fill="tozeroy",
            fillcolor="rgba(32, 197, 99, 0.12)",
        )
    )

    fig.update_layout(**_base_layout())

    fig.update_xaxes(showgrid=False, showline=False, tickfont=dict(color=MUTED))
    fig.update_yaxes(showgrid=True, gridcolor=GRID, zeroline=False)

    return fig


def multi_line_chart(x_values, series: dict, colors=None):
    """Multiple named line series on one chart, e.g. temperature/humidity/power."""

    if colors is None:
        colors = [GREEN, BLUE, ORANGE, RED]

    fig = go.Figure()

    for index, (name, y_values) in enumerate(series.items()):

        fig.add_trace(
            go.Scatter(
                x=x_values,
                y=y_values,
                mode="lines",
                name=name,
                line=dict(
                    color=colors[index % len(colors)],
                    width=2.5,
                    shape="spline",
                    smoothing=0.5,
                ),
            )
        )

    fig.update_layout(**_base_layout(height=300, show_legend=True))

    fig.update_xaxes(showgrid=False, showline=False, tickfont=dict(color=MUTED))
    fig.update_yaxes(showgrid=True, gridcolor=GRID, zeroline=False)

    return fig


def donut_chart(labels, values, colors=None):
    """A clean donut chart, e.g. resolved vs unresolved alerts."""

    if colors is None:
        colors = [GREEN, RED, ORANGE, BLUE][: len(labels)]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.62,
                marker=dict(colors=colors, line=dict(color="#ffffff", width=2)),
                textinfo="label+percent",
                textfont=dict(color=NAVY, size=12),
            )
        ]
    )

    fig.update_layout(**_base_layout(height=280, show_legend=True))

    return fig


def bar_chart(categories, values, color=BLUE, horizontal=False):
    """A clean bar chart, e.g. failure counts by type."""

    fig = go.Figure()

    if horizontal:
        fig.add_trace(
            go.Bar(
                y=categories,
                x=values,
                orientation="h",
                marker=dict(color=color, cornerradius=6),
            )
        )
        fig.update_xaxes(showgrid=True, gridcolor=GRID, zeroline=False)
        fig.update_yaxes(showgrid=False)
    else:
        fig.add_trace(
            go.Bar(
                x=categories,
                y=values,
                marker=dict(color=color, cornerradius=6),
            )
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor=GRID, zeroline=False)

    fig.update_layout(**_base_layout())

    return fig
