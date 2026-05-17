# AirAlert Presentation Guide

This guide helps present AirAlert as a final QUA3CK-based ML Streamlit app.

## 1. One-sentence pitch

AirAlert predicts urban air-quality risk by combining pollution indicators, weather context and city-structure variables into an interactive Streamlit dashboard.

## 2. Why this project?

Air-quality values such as PM2.5, PM10, NO2 and O3 are technically meaningful, but not immediately understandable for non-expert users. AirAlert solves this by translating multiple environmental data layers into a clear risk class: Low, Medium or High.

## 3. Similarity to Noah's project

Noah's app translates complex climate data into local climate-risk views. AirAlert follows the same pattern in a smaller context:

```text
multiple data layers -> ML model -> risk prediction -> Streamlit dashboard -> knowledge transfer
```

## 4. QUA3CK explanation

### Q - Question

The guiding question is: how can air-quality, weather and city-context data be combined to predict urban air-quality risk for non-experts?

### U - Understanding the Data

The app uses three data layers:

- Air quality: PM2.5, PM10, NO2, O3.
- Weather: temperature, humidity, wind speed.
- City context: population, traffic, green space, industry.

The classroom version uses deterministic operational data for stability. The structure maps to real public sources such as OpenAQ, Open-Meteo and city metadata datasets.

### A - Algorithm, Adapting, Adjusting

The app uses a Random Forest classifier. It is appropriate because the target is a class: Low, Medium or High. Features are adapted through city encoding, seasonality through month and combined pollutant/weather/context variables.

### C - Conclude

The app evaluates the model with accuracy, confusion matrix, classification report and feature importance. It also explains limitations clearly.

### K - Knowledge Transfer

The Streamlit app turns the model into a usable dashboard with sliders, charts, risk labels, downloads and plain-language explanations.

## 5. Demo flow

1. Start on Dashboard and explain the risk card.
2. Change the city and month in the sidebar.
3. Open Prediction Lab and move pollutant/weather sliders.
4. Show Model Evaluation and feature importance.
5. Open Sources & Export and explain the three data layers.
6. Open QUA3CK Process and walk through the phases.

## 6. Limitations to state honestly

- The current version uses deterministic operational data for reliability.
- It is an educational ML prototype, not an official health-warning system.
- The AQI-like score is simplified.
- Street-level micro-effects are not modeled.

## 7. Strong closing sentence

AirAlert shows how the QUA3CK process can turn a clear environmental question into a working ML application that is understandable, interactive and ready for deployment.
