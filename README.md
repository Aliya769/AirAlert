# AirAlert: Urban Air Quality Risk Navigator

AirAlert is a compact machine-learning Streamlit app inspired by the structure of Noah Roosen's "Degrees of No Return" example project, but adapted to a smaller context: urban air quality.

The project follows the QUA3CK process from the course material: Question, Understanding the Data, Algorithm/Adapting/Adjusting, Conclude and Knowledge Transfer.

The app combines three data layers:

- Air quality indicators: PM2.5, PM10, NO2, O3 and AQI risk class.
- Weather context: temperature, humidity and wind speed.
- City context: population, traffic, green space and industry indices.

The goal is to predict whether a selected city and scenario has a low, medium or high air quality risk.

## Files

```text
airalert_app/
+-- app.py
+-- requirements.txt
+-- README.md
+-- DATA_SOURCES.md
+-- PRESENTATION_GUIDE.md
+-- src/
|   +-- data_factory.py
|   +-- modeling.py
|   +-- visuals.py
+-- notebooks/
    +-- Q-Phase.ipynb
    +-- U-Phase.ipynb
    +-- A-Phase.ipynb
    +-- C-Phase.ipynb
    +-- K-Phase.md
    +-- Colab-Test.ipynb
```

## Streamlit Cloud

For deployment, select:

```text
app.py
```

as the main file in Streamlit Cloud.

## Local or Colab Test

Install requirements:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
python -m streamlit run app.py
```

## QUA3CK Logic

The project follows the five-phase QUA3CK process:

- Q: define the air-quality risk question.
- U: explain pollutant, weather and city-context data.
- A1: select the Random Forest classifier.
- A2: adapt features such as city, month, weather and pollutants.
- A3: adjust model settings for stable prediction.
- C: evaluate the model and state limitations.
- K: transfer the model into the Streamlit dashboard.

## Data Sources

The current app uses deterministic demo data so it works reliably without API keys or external downloads. The data structure mirrors three public-data layers:

- OpenAQ-style air-quality data.
- Open-Meteo-style weather data.
- World Cities / GeoNames-style city metadata.

See `DATA_SOURCES.md` for the full explanation.

## Presentation Readiness

The app is ready to be presented as a complete QUA3CK-based Streamlit ML application. For the final presentation, use:

- `PRESENTATION_GUIDE.md` for the speaking structure.
- `notebooks/Q-Phase.ipynb` through `notebooks/C-Phase.ipynb` for the notebook documentation.
- `notebooks/K-Phase.md` for the knowledge-transfer/deployment explanation.
- the in-app `QUA3CK Process` page for a live walkthrough.

## Disclaimer

This is a classroom ML prototype with deterministic demo data. It is not an official health, medical or regulatory air-quality warning system.
