# K-Phase: Knowledge Transfer and Streamlit Deployment

This document describes the final QUA3CK phase of **AirAlert**. The K-phase transfers the work from the Q, U, A and C phases into a stable, understandable and deployed Streamlit application.

---

## 1. Goal of the K-Phase

The goal of the K-phase is to make the machine-learning workflow usable for people who are not working inside the notebooks. The result should not remain a technical model hidden in Python cells. It should become an interactive dashboard that explains urban air-quality risk clearly.

For AirAlert, knowledge transfer means:

- raw pollutant, weather and city-structure values become a simple risk label,
- the model output becomes visible through metrics, charts and explanations,
- users can test realistic city-month scenarios with sliders,
- model quality is shown through evaluation outputs,
- limitations are explained so the prediction is not overclaimed.

**Main K-phase question:**

How can the AirAlert model be turned into a reliable Streamlit app that communicates urban pollution risk in an understandable and presentation-ready way?

---

## 2. Architecture and Frontend Development

AirAlert uses **Streamlit** as the deployment technology. Streamlit is suitable for this project because it connects the Python data-science workflow directly with an interactive web interface.

The deployed app combines:

- a generated pandas dataset,
- a scikit-learn classification model,
- Plotly visualisations,
- Streamlit controls and metrics,
- export options for CSV and JSON,
- transparent explanations of data sources and limitations.

The main deployment file is:

```text
app.py
```

For local execution and Streamlit Cloud deployment, `app.py` is the entry point.

---

## 3. Application Structure

The app is split into one Streamlit file and helper modules:

```text
app.py
src/data_factory.py
src/modeling.py
src/visuals.py
```

This structure keeps the app maintainable. The notebooks explain and validate the workflow, while the app files contain the reusable production logic.

### 3.1 `app.py`

`app.py` is the frontend and navigation layer. It:

- configures the Streamlit page,
- loads the AirAlert dataset,
- trains or reuses the cached model,
- creates sidebar inputs,
- routes users through the app pages,
- displays metrics, charts, predictions and downloads.

### 3.2 `src/data_factory.py`

`data_factory.py` creates the deterministic AirAlert dataset. It contains:

- city profiles,
- monthly weather context,
- pollutant values,
- an AQI-like score,
- the target label `risk_level`,
- scenario defaults for the Prediction Lab.

This module is important because the classroom version must run smoothly without relying on unstable live APIs.

### 3.3 `src/modeling.py`

`modeling.py` contains the machine-learning workflow. It:

- defines the model features,
- builds preprocessing for categorical and numeric variables,
- trains the Random Forest classifier,
- evaluates the model,
- returns class probabilities,
- creates feature-importance tables.

The final model predicts the target classes:

```text
Low / Medium / High
```

### 3.4 `src/visuals.py`

`visuals.py` contains reusable chart logic. It creates:

- city trend charts,
- city comparison charts,
- prediction probability charts,
- feature-importance charts,
- risk-based colours.

Separating visuals from model code makes the app easier to test and update.

---

## 4. User Interface and User Guidance

The Streamlit interface is built as a dashboard with clear pages instead of one long technical output.

The sidebar controls:

- page navigation,
- city selection,
- month selection,
- scenario sliders for traffic, green space, industry, weather and pollutants.

The app pages are:

- Dashboard,
- Project Story,
- Data Explorer,
- Prediction Lab,
- Model Evaluation,
- Sources & Export,
- QUA3CK Process.

Each page transfers a different part of the notebook work into a user-facing format.

---

## 5. Dashboard

The Dashboard gives the quickest interpretation of the model result. It shows:

- predicted risk level,
- estimated AQI-like score,
- model accuracy,
- dataset size,
- selected city summary,
- city trend chart,
- city comparison chart,
- map-based city context.

This page is designed for fast understanding. A user should immediately know whether the chosen city-month situation is low, medium or high risk.

---

## 6. Project Story

The Project Story page explains why AirAlert exists. It translates the technical project into a problem narrative:

- pollution values are difficult to interpret alone,
- urban air risk depends on pollutant, weather and city-structure factors,
- the app converts these inputs into a clear risk category,
- the result supports learning, presentation and decision awareness.

This page is the bridge between the Q-phase question and the deployed product.

---

## 7. Data Explorer

The Data Explorer transfers the U-phase into the app.

It shows:

- dataset layers,
- selected city profile,
- city-level trend visualisation,
- filtered data table,
- CSV export for the selected city.

This makes the dataset transparent. Users can inspect what the model is based on instead of only seeing a final prediction.

---

## 8. Prediction Lab

The Prediction Lab is the core interactive ML feature.

Users can change scenario values and observe how the model reacts. The page shows:

- current input scenario,
- predicted risk label,
- prediction probabilities for Low, Medium and High,
- downloadable CSV output,
- downloadable JSON output.

This is the strongest knowledge-transfer component because users can test "what if" situations themselves.

---

## 9. Model Evaluation

The Model Evaluation page transfers the C-phase into the deployed app.

It shows:

- test accuracy,
- classification report,
- confusion matrix,
- feature importance.

This page supports transparency. It makes clear that AirAlert is not only producing labels, but that the model was evaluated and checked before deployment.

---

## 10. Sources and Export

The Sources & Export page explains the dataset strategy and export options.

It communicates:

- which data layers are represented,
- how public data sources could map to the classroom dataset,
- why the deployed version uses deterministic data,
- how users can export the current prediction,
- how users can export the generated dataset.

This prevents a common misunderstanding: the app is stable and presentation-ready, but it is not a live official air-quality monitoring system.

---

## 11. ML Integration

The model from the A- and C-phases is integrated into the Streamlit workflow through reusable functions.

The final pipeline uses:

- city as categorical context,
- month as seasonal context,
- city structure features,
- weather features,
- pollutant features,
- a Random Forest classifier for the deployed explanation workflow.

The C-phase validation showed that the final model is strong enough for the app context:

```text
Accuracy: 0.854
Macro-F1: 0.802
Decision: GO
```

The model is also interpretable enough for presentation because feature importance can be shown directly in the app.

---

## 12. Deployment and Local Run

The deployed app is available through Streamlit Cloud:

```text
https://airalert.streamlit.app/
```

For local execution, the project should be opened in the AirAlert project folder and started with:

```powershell
cd "C:\Users\aliya\Documents\Codex\2026-05-15\files-mentioned-by-the-user-python\airalert_app - CopyPresentReady\airalert_app"
C:\Users\aliya\Documents\Codex\airalert_venv\Scripts\python.exe -m streamlit run app.py
```

Important environment note:

- use the AirAlert Python environment,
- do not use the old broken Python 3.14 environment,
- notebooks should use the `AirAlert (Python 3.13)` kernel.

The K-phase itself is Markdown documentation, so it does not create notebook runtime errors.

---

## 13. Limitations

AirAlert is a presentation-ready data-science app, but it has clear limitations:

- the dataset is deterministic and generated for the project,
- values are AQI-like and simplified,
- street-level microclimate is not modelled,
- live sensors and official APIs are not connected in the current version,
- predictions support interpretation and learning, not official health warnings.

These limitations are part of the knowledge transfer. The app should be useful without pretending to be more precise than it is.

---

## 14. Result

The K-phase closes the gap between notebook analysis and user-facing application.

AirAlert now transfers the Q, U, A and C phases into a working Streamlit product:

- Q-phase: the air-quality risk question is visible in the app story,
- U-phase: the dataset is explorable through tables and charts,
- A-phase: model selection is represented through the final classifier,
- C-phase: quality checks are shown through evaluation metrics,
- K-phase: the complete workflow is communicated through a deployed dashboard.

The final result is a stable, understandable and presentation-ready Streamlit application for urban air-quality risk communication.
