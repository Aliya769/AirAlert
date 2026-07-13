# Q-Phase: Question and Problem Definition

This document describes the Question phase of **AirAlert**, a QUA3CK-based Streamlit machine-learning app for urban air-quality risk prediction. The Q-phase defines the problem, target users, guiding question and success criteria before any data generation or model training happens.

---

## 1. Purpose of the Q-Phase

The goal of the Q-phase is to turn a broad environmental concern into a clear machine-learning task. Air quality is a real urban issue, but the project needs a focused question that can be answered with structured data and communicated in an app.

AirAlert focuses on a practical classroom prototype:

- combine pollutant, weather and city-context indicators,
- train a model that predicts a simple risk class,
- explain the result to non-expert users through Streamlit.

The project therefore does not try to become an official health-warning system. It is an educational ML dashboard that demonstrates the full QUA3CK workflow in a stable and presentable form.

---

## 2. Main Research Question

The guiding question is:

**How can pollution, weather and city-context data be combined into a simple machine-learning tool that predicts urban air-quality risk for non-expert users?**

This question is suitable for a Streamlit ML app because it contains:

- a real-world topic: urban air quality,
- multiple data layers: pollutants, weather and city context,
- a clear prediction target: Low, Medium or High risk,
- a user-facing output: an understandable risk signal.

---

## 3. Problem Background

Air-quality measurements often appear as technical numbers. Values such as PM2.5, PM10, NO2 and O3 are important, but they are difficult to interpret without environmental or medical background knowledge.

For example, a user may see a PM2.5 value and not immediately know whether the situation is acceptable, concerning or dangerous. AirAlert addresses this communication problem by translating several indicators into a simple risk category.

The problem is not only technical. It is also about knowledge transfer:

- raw data must become understandable,
- model output must be visible and interactive,
- limitations must be stated clearly,
- users should not mistake the prototype for official advice.

---

## 4. Target Users

The app is designed for non-expert users in an educational or presentation context.

Important user groups are:

- classmates and teachers evaluating the project,
- citizens who want a simple air-quality explanation,
- students learning how ML workflows become apps,
- presenters who need to explain QUA3CK through a working example.

The interface therefore prioritizes clarity over technical density. The app uses risk labels, charts, metrics, sliders and download buttons instead of only notebooks and tables.

---

## 5. Project Scope

AirAlert predicts a simplified air-quality risk class for selected European cities and user-adjustable scenarios.

Included in scope:

- deterministic classroom dataset,
- pollutant indicators,
- weather indicators,
- city-context indicators,
- Random Forest classification,
- model evaluation,
- Streamlit dashboard,
- downloadable outputs,
- transparent limitations.

Outside the current scope:

- live API calls,
- street-level pollution mapping,
- official AQI certification,
- medical recommendations,
- real-time government alerts.

This scoped version is intentional because the app must run smoothly in Streamlit Cloud without API keys, rate limits or notebook execution errors.

---

## 6. Prediction Target

The model predicts:

```text
risk_level = Low, Medium or High
```

This target is derived from an AQI-like score created inside the data factory. The score combines pollutant concentration, humidity, wind and seasonality into an interpretable risk scale.

The target is appropriate for classification because the user does not need an exact technical measurement first. The main user question is:

```text
Is this scenario low, medium or high risk?
```

---

## 7. Success Criteria

The Q-phase defines what a successful project should deliver.

A successful AirAlert version should:

- open without runtime errors on Streamlit Cloud,
- show a clear risk prediction,
- allow users to change city, month and scenario values,
- explain the data layers,
- evaluate the model with accuracy and confusion matrix,
- show feature importance,
- provide downloads for transparency,
- document all QUA3CK phases in readable Markdown.

---

## 8. Q-Phase Output

The output of this phase is the project foundation:

- topic: urban air-quality risk,
- main question: predicting risk from multiple data layers,
- target: Low, Medium or High risk class,
- user group: non-expert educational users,
- final product: stable Streamlit ML app.

This foundation guides the U, A, C and K phases.
