from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


RISK_COLORS = {"Low": "#2e7d32", "Medium": "#f9a825", "High": "#c62828"}


def risk_badge_color(risk: str) -> str:
    return RISK_COLORS.get(risk, "#546e7a")


def trend_chart(df: pd.DataFrame, city: str) -> go.Figure:
    city_df = df[df["city"] == city].sort_values("date")
    fig = px.line(
        city_df,
        x="date",
        y=["aqi_score", "pm25", "no2"],
        labels={"value": "Index / concentration", "date": "Date", "variable": "Metric"},
        title=f"Air quality trend for {city}",
    )
    fig.update_layout(height=380, legend_orientation="h", margin=dict(l=10, r=10, t=55, b=10))
    return fig


def city_comparison_chart(df: pd.DataFrame) -> go.Figure:
    grouped = (
        df.groupby("city", as_index=False)
        .agg(aqi_score=("aqi_score", "mean"), pm25=("pm25", "mean"), no2=("no2", "mean"))
        .sort_values("aqi_score", ascending=False)
    )
    fig = px.bar(
        grouped,
        x="city",
        y="aqi_score",
        color="aqi_score",
        color_continuous_scale=["#2e7d32", "#f9a825", "#c62828"],
        title="Average air quality risk by city",
        labels={"aqi_score": "Average AQI score", "city": "City"},
    )
    fig.update_layout(height=360, margin=dict(l=10, r=10, t=55, b=10))
    return fig


def feature_importance_chart(feature_table: pd.DataFrame) -> go.Figure:
    table = feature_table.sort_values("importance", ascending=True)
    fig = px.bar(
        table,
        x="importance",
        y="feature",
        orientation="h",
        title="Most important model features",
        labels={"importance": "Importance", "feature": "Feature"},
        color="importance",
        color_continuous_scale=["#90caf9", "#1565c0"],
    )
    fig.update_layout(height=420, margin=dict(l=10, r=10, t=55, b=10), showlegend=False)
    return fig


def probability_chart(probabilities: dict[str, float]) -> go.Figure:
    ordered = ["Low", "Medium", "High"]
    values = [probabilities.get(label, 0) for label in ordered]
    fig = px.bar(
        x=ordered,
        y=values,
        color=ordered,
        color_discrete_map=RISK_COLORS,
        labels={"x": "Risk class", "y": "Model probability"},
        title="Prediction confidence",
    )
    fig.update_yaxes(range=[0, 1], tickformat=".0%")
    fig.update_layout(height=300, margin=dict(l=10, r=10, t=55, b=10), showlegend=False)
    return fig
