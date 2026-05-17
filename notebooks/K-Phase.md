# AirAlert: K-Phase - Knowledge Transfer and Streamlit App

The K-phase transfers the data-science workflow into a usable Streamlit application. This is the final step in QUA3CK: the result should not remain hidden in notebooks, but become understandable and interactive.

## Goal

The goal of AirAlert is to communicate urban air-quality risk to non-expert users. Instead of showing only raw pollutant tables, the app provides a clear risk class, charts, model evaluation and downloadable outputs.

## Streamlit structure

The app contains six pages:

- Dashboard: main prediction, metrics, trend chart and city map.
- Data Explorer: dataset layers, current city profile and city-level table.
- Prediction Lab: adjustable scenario inputs and prediction probabilities.
- Model Evaluation: accuracy, confusion matrix, classification report and feature importance.
- Sources & Export: data-source explanation and CSV downloads.
- QUA3CK Process: short explanation of all project phases.

## Knowledge transfer logic

The app translates a technical ML process into a usable interface:

- sliders make scenarios understandable,
- risk labels simplify interpretation,
- charts show trends and comparisons,
- evaluation results make the model transparent,
- disclaimers prevent overclaiming.

## Deployment

The app is designed for Streamlit Cloud. The main file is `app.py`, and dependencies are listed in `requirements.txt`. No API keys are required for the stable classroom version.

## Final note

AirAlert is a presentable educational ML app. It demonstrates the full QUA3CK movement from research question to deployed knowledge transfer while remaining smaller and easier to explain than the larger climate-risk example project.
