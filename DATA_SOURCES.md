# AirAlert Data Source Explanation

AirAlert uses three dataset layers. In the stable classroom version, these layers are generated deterministically inside the project so the app runs without API keys, external downloads or broken links. This makes the project reliable for PyCharm, Streamlit Cloud and presentation use.

## 1. Air-quality layer

Columns in the app:

- `pm25`
- `pm10`
- `no2`
- `o3`
- `aqi_score`
- `risk_level`

Meaning: these variables represent pollutant concentration and the derived Low/Medium/High risk class.

Suggested real public source for a future version: OpenAQ or comparable air-quality measurement datasets.

## 2. Weather layer

Columns in the app:

- `temperature_c`
- `humidity_pct`
- `wind_kmh`
- `month`

Meaning: weather conditions can amplify or reduce pollution risk. Wind can disperse pollutants, while seasonal patterns can influence particulate matter and ozone.

Suggested real public source for a future version: Open-Meteo historical weather data.

## 3. City-context layer

Columns in the app:

- `city`
- `country`
- `latitude`
- `longitude`
- `population_m`
- `traffic_index`
- `green_space_index`
- `industrial_index`

Meaning: city structure affects pollution pressure. Traffic and industry can increase risk, while green space can reduce it.

Suggested real public sources for a future version: World Cities, GeoNames, city open-data portals or public urban indicator datasets.

## Why deterministic demo data?

The professor requires several datasets as the foundation of the app. AirAlert models three separate data layers and keeps them visible in the app. For the first presentable version, deterministic data is used because it guarantees reproducibility and avoids technical failure during presentation.

This is similar to building a controlled prototype first. Later, the same structure can be connected to live or downloaded public datasets.

## Relation to QUA3CK

- Q: the question defines why air-quality risk should be predicted.
- U: the dataset layers are explored and explained.
- A: the model learns from pollutant, weather and city-context features.
- C: the model is evaluated and limitations are stated.
- K: the app communicates the result through Streamlit.
