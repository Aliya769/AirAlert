# U-Phase: Understanding the Data

This upgraded U-phase follows the Degrees of No Return reference structure more closely: it does not only describe the data, it also explores it, checks it and prepares it for modeling.

## Improvements Made

- Added a task-by-task EDA structure.
- Added first visual checks for city risk, class distribution and monthly patterns.
- Added stronger quality checks for missing values, duplicates, data types and expected columns.
- Added an explicit target-leakage warning: `aqi_score` explains the target but should not be used as a model feature.
- Added a feature-readiness section for the A-phase.
- Added a clear go decision for modeling.

## Main Data Layers

- Air quality: `pm25`, `pm10`, `no2`, `o3`, `aqi_score`, `risk_level`
- Weather: `temperature_c`, `humidity_pct`, `wind_kmh`, `month`
- City context: `population_m`, `traffic_index`, `green_space_index`, `industrial_index`

## U-Phase Decision

The dataset is ready for the A-phase because it has clear feature groups, a clear target variable, no blocking missing-value issue and a stable deterministic generation process for deployment.
