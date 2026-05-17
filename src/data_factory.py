from __future__ import annotations

import numpy as np
import pandas as pd


CITY_PROFILES = pd.DataFrame(
    [
        {
            "city": "Berlin",
            "country": "Germany",
            "latitude": 52.52,
            "longitude": 13.405,
            "population_m": 3.76,
            "traffic_index": 58,
            "green_space_index": 46,
            "industrial_index": 38,
        },
        {
            "city": "Paris",
            "country": "France",
            "latitude": 48.8566,
            "longitude": 2.3522,
            "population_m": 2.16,
            "traffic_index": 73,
            "green_space_index": 32,
            "industrial_index": 44,
        },
        {
            "city": "London",
            "country": "United Kingdom",
            "latitude": 51.5072,
            "longitude": -0.1276,
            "population_m": 8.98,
            "traffic_index": 78,
            "green_space_index": 40,
            "industrial_index": 41,
        },
        {
            "city": "Madrid",
            "country": "Spain",
            "latitude": 40.4168,
            "longitude": -3.7038,
            "population_m": 3.22,
            "traffic_index": 64,
            "green_space_index": 35,
            "industrial_index": 36,
        },
        {
            "city": "Milan",
            "country": "Italy",
            "latitude": 45.4642,
            "longitude": 9.19,
            "population_m": 1.35,
            "traffic_index": 82,
            "green_space_index": 28,
            "industrial_index": 66,
        },
        {
            "city": "Warsaw",
            "country": "Poland",
            "latitude": 52.2297,
            "longitude": 21.0122,
            "population_m": 1.79,
            "traffic_index": 62,
            "green_space_index": 39,
            "industrial_index": 58,
        },
        {
            "city": "Amsterdam",
            "country": "Netherlands",
            "latitude": 52.3676,
            "longitude": 4.9041,
            "population_m": 0.92,
            "traffic_index": 49,
            "green_space_index": 44,
            "industrial_index": 33,
        },
        {
            "city": "Vienna",
            "country": "Austria",
            "latitude": 48.2082,
            "longitude": 16.3738,
            "population_m": 1.9,
            "traffic_index": 45,
            "green_space_index": 51,
            "industrial_index": 29,
        },
    ]
)


def classify_aqi(aqi: float) -> str:
    if aqi < 45:
        return "Low"
    if aqi < 75:
        return "Medium"
    return "High"


def estimate_aqi_score(values: dict[str, float]) -> float:
    """Estimate an interpretable AQI-like score from one scenario row."""

    month = int(values["month"])
    winter = 1 if month in [11, 12, 1, 2] else 0
    aqi_score = (
        0.95 * float(values["pm25"])
        + 0.38 * float(values["pm10"])
        + 0.48 * float(values["no2"])
        + 0.22 * float(values["o3"])
        + float(values["humidity_pct"]) * 0.12
        - float(values["wind_kmh"]) * 0.65
        + winter * 7
    )
    return round(float(np.clip(aqi_score, 15, 160)), 1)


def build_airalert_dataset(seed: int = 42) -> pd.DataFrame:
    """Create a stable multi-source demo dataset for the app.

    The columns represent three dataset layers:
    air quality measurements, weather context, and city structure.
    Values are deterministic and shaped to be realistic enough for a
    classroom ML prototype, while avoiding fragile external API calls.
    """

    rng = np.random.default_rng(seed)
    months = pd.date_range("2020-01-01", "2025-12-01", freq="MS")
    rows: list[dict[str, object]] = []

    for _, city in CITY_PROFILES.iterrows():
        for date in months:
            month = int(date.month)
            winter = 1 if month in [11, 12, 1, 2] else 0
            summer = 1 if month in [6, 7, 8] else 0
            seasonal_wave = np.sin((month - 1) / 12 * 2 * np.pi)

            temp_c = 11 + 11 * seasonal_wave + (city.latitude - 48) * -0.25 + rng.normal(0, 1.8)
            humidity_pct = 62 - 10 * seasonal_wave + winter * 7 + rng.normal(0, 5)
            wind_kmh = 13 + rng.normal(0, 3) + (city.green_space_index / 100) * 2

            traffic = float(city.traffic_index)
            industry = float(city.industrial_index)
            green = float(city.green_space_index)

            pm25 = 6 + traffic * 0.16 + industry * 0.14 + winter * 9 - wind_kmh * 0.25 - green * 0.05
            pm10 = 12 + traffic * 0.22 + industry * 0.16 + winter * 7 - wind_kmh * 0.18
            no2 = 10 + traffic * 0.34 + industry * 0.09 + winter * 4 - wind_kmh * 0.12
            o3 = 28 + summer * 20 + temp_c * 0.7 - no2 * 0.18

            pm25 = max(2, pm25 + rng.normal(0, 3.0))
            pm10 = max(5, pm10 + rng.normal(0, 4.5))
            no2 = max(3, no2 + rng.normal(0, 5.0))
            o3 = max(5, o3 + rng.normal(0, 6.0))

            aqi_score = estimate_aqi_score(
                {
                    "month": month,
                    "pm25": pm25,
                    "pm10": pm10,
                    "no2": no2,
                    "o3": o3,
                    "humidity_pct": humidity_pct,
                    "wind_kmh": wind_kmh,
                }
            )

            rows.append(
                {
                    "date": date,
                    "year": int(date.year),
                    "month": month,
                    "city": city.city,
                    "country": city.country,
                    "latitude": float(city.latitude),
                    "longitude": float(city.longitude),
                    "population_m": float(city.population_m),
                    "traffic_index": traffic,
                    "green_space_index": green,
                    "industrial_index": industry,
                    "temperature_c": round(float(temp_c), 1),
                    "humidity_pct": round(float(np.clip(humidity_pct, 25, 95)), 1),
                    "wind_kmh": round(float(np.clip(wind_kmh, 2, 35)), 1),
                    "pm25": round(float(pm25), 1),
                    "pm10": round(float(pm10), 1),
                    "no2": round(float(no2), 1),
                    "o3": round(float(o3), 1),
                    "aqi_score": round(aqi_score, 1),
                    "risk_level": classify_aqi(aqi_score),
                }
            )

    return pd.DataFrame(rows)


def scenario_from_city_month(df: pd.DataFrame, city: str, month: int) -> dict[str, float]:
    subset = df[(df["city"] == city) & (df["month"] == month)]
    if subset.empty:
        subset = df[df["city"] == city]
    numeric_cols = [
        "temperature_c",
        "humidity_pct",
        "wind_kmh",
        "pm25",
        "pm10",
        "no2",
        "o3",
        "traffic_index",
        "green_space_index",
        "industrial_index",
        "population_m",
    ]
    return subset[numeric_cols].mean().to_dict()
