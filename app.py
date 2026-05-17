from __future__ import annotations

import json

import pandas as pd
import streamlit as st

from src.data_factory import CITY_PROFILES, build_airalert_dataset, estimate_aqi_score, scenario_from_city_month
from src.modeling import feature_importance_table, predict_risk, train_air_quality_model
from src.visuals import (
    city_comparison_chart,
    feature_importance_chart,
    probability_chart,
    risk_badge_color,
    trend_chart,
)


st.set_page_config(page_title="AirAlert", page_icon=":material/air:", layout="wide")


@st.cache_data
def load_data() -> pd.DataFrame:
    return build_airalert_dataset()


@st.cache_resource
def load_model(df: pd.DataFrame) -> dict[str, object]:
    return train_air_quality_model(df)


df = load_data()
model_bundle = load_model(df)
model = model_bundle["model"]

st.sidebar.title("AirAlert")
st.sidebar.caption("Urban Air Quality Risk Navigator")
page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Project Story",
        "Data Explorer",
        "Prediction Lab",
        "Model Evaluation",
        "Sources & Export",
        "QUA3CK Process",
    ],
)

st.sidebar.divider()
city = st.sidebar.selectbox("City", sorted(df["city"].unique()), index=0)
month = st.sidebar.slider("Month", 1, 12, 6)


def sidebar_scenario() -> dict[str, object]:
    base = scenario_from_city_month(df, city, month)
    selected_city = CITY_PROFILES[CITY_PROFILES["city"] == city].iloc[0].to_dict()

    st.sidebar.markdown("### Scenario inputs")
    values = {
        "city": city,
        "month": month,
        "population_m": float(selected_city["population_m"]),
        "traffic_index": float(selected_city["traffic_index"]),
        "green_space_index": float(selected_city["green_space_index"]),
        "industrial_index": float(selected_city["industrial_index"]),
        "temperature_c": st.sidebar.slider("Temperature C", -5.0, 38.0, float(base["temperature_c"]), 0.5),
        "humidity_pct": st.sidebar.slider("Humidity %", 20.0, 95.0, float(base["humidity_pct"]), 1.0),
        "wind_kmh": st.sidebar.slider("Wind km/h", 1.0, 35.0, float(base["wind_kmh"]), 0.5),
        "pm25": st.sidebar.slider("PM2.5", 2.0, 80.0, float(base["pm25"]), 0.5),
        "pm10": st.sidebar.slider("PM10", 5.0, 120.0, float(base["pm10"]), 0.5),
        "no2": st.sidebar.slider("NO2", 3.0, 90.0, float(base["no2"]), 0.5),
        "o3": st.sidebar.slider("O3", 5.0, 100.0, float(base["o3"]), 0.5),
    }
    return values


scenario_values = sidebar_scenario()
prediction, probabilities = predict_risk(model, scenario_values)
estimated_aqi = estimate_aqi_score(scenario_values)
badge_color = risk_badge_color(prediction)


def show_prediction_summary() -> None:
    st.markdown(
        f"""
        <div style="padding:18px;border-left:8px solid {badge_color};background:#f7f9fb;border-radius:6px">
            <div style="font-size:14px;color:#546e7a">Predicted air quality risk</div>
            <div style="font-size:36px;font-weight:700;color:{badge_color}">{prediction}</div>
            <div style="font-size:15px;color:#263238">Estimated AQI-like score: <b>{estimated_aqi}</b>. Based on pollution, weather and city-context indicators.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def current_scenario_frame() -> pd.DataFrame:
    row = dict(scenario_values)
    row["predicted_risk"] = prediction
    row["estimated_aqi_score"] = estimated_aqi
    for label, value in probabilities.items():
        row[f"probability_{label.lower()}"] = round(value, 4)
    return pd.DataFrame([row])


if page == "Dashboard":
    st.title("AirAlert: Urban Air Quality Risk Navigator")
    st.write(
        "A compact QUA3CK-based machine-learning app that translates pollution, weather and city "
        "context data into an understandable air-quality risk signal."
    )

    col1, col2, col3 = st.columns([1.2, 1, 1])
    with col1:
        show_prediction_summary()
    with col2:
        st.metric("Model accuracy", f"{model_bundle['accuracy']:.1%}")
        st.metric("Rows in demo dataset", f"{len(df):,}")
    with col3:
        selected = df[df["city"] == city]
        st.metric("Average AQI score", f"{selected['aqi_score'].mean():.1f}")
        high_share = (selected["risk_level"] == "High").mean()
        st.metric("High-risk months", f"{high_share:.0%}")

    st.plotly_chart(trend_chart(df, city), width="stretch")
    st.subheader("City map")
    st.map(CITY_PROFILES.rename(columns={"latitude": "lat", "longitude": "lon"}), latitude="lat", longitude="lon")
    st.plotly_chart(city_comparison_chart(df), width="stretch")

elif page == "Project Story":
    st.title("Project Story")
    st.write(
        "AirAlert is designed as a smaller, presentation-ready counterpart to the climate-risk example project. "
        "The central transfer idea is the same: complex environmental data becomes an interactive risk dashboard."
    )

    st.subheader("Problem")
    st.write(
        "Air-quality data is often shown as technical pollutant values. For non-expert users, values such as "
        "PM2.5, NO2 or O3 are hard to interpret. AirAlert turns these inputs into a clear Low, Medium or High "
        "risk class and explains the model result visually."
    )

    st.subheader("App logic")
    st.markdown(
        """
        1. Combine three data layers: air quality, weather and city context.
        2. Train a Random Forest classifier on tabular scenario data.
        3. Let users change the scenario with sliders.
        4. Show the predicted risk class, probabilities, trends and model evaluation.
        5. Communicate limitations transparently.
        """
    )

    st.subheader("Connection to Noah's example")
    st.markdown(
        """
        - Noah's app: climate data -> local heat/flooding risk -> climate dashboard.
        - AirAlert: pollution/weather/city data -> air-quality risk -> urban health/environment dashboard.
        - Both apps: multiple data layers -> ML model -> Streamlit dashboard -> understandable risk communication.
        """
    )

    st.subheader("Final presentation message")
    st.info(
        "AirAlert demonstrates the full QUA3CK workflow on a manageable environmental ML problem: from a clear "
        "question, through data understanding and model choice, to evaluation and knowledge transfer in Streamlit."
    )

elif page == "Data Explorer":
    st.title("Data Explorer")
    st.write(
        "The U-phase logic of AirAlert is based on three data layers. Each layer has a clear role "
        "in the later machine-learning prediction."
    )

    left, right = st.columns([1, 1])
    with left:
        st.subheader("Dataset layers")
        st.markdown(
            """
            - Air quality: PM2.5, PM10, NO2, O3 and AQI risk class.
            - Weather: temperature, humidity and wind speed.
            - City context: population, traffic, green space and industry indices.
            - Target: Low, Medium or High air-quality risk.
            """
        )
    with right:
        st.subheader("Current city profile")
        profile = CITY_PROFILES[CITY_PROFILES["city"] == city].T.reset_index()
        profile.columns = ["field", "value"]
        profile["value"] = profile["value"].astype(str)
        st.dataframe(profile, width="stretch", hide_index=True)

    filtered = df[df["city"] == city].sort_values("date")
    st.plotly_chart(trend_chart(df, city), width="stretch")
    st.download_button(
        "Download filtered city data as CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name=f"airalert_{city.lower()}_data.csv",
        mime="text/csv",
    )
    st.dataframe(filtered, width="stretch", hide_index=True)

elif page == "Prediction Lab":
    st.title("Prediction Lab")
    st.write(
        "Adjust the scenario in the sidebar and watch how the trained model classifies air-quality risk. "
        "This page is the interactive part of the Knowledge Transfer phase."
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        show_prediction_summary()
        st.subheader("Scenario values")
        scenario_table = pd.DataFrame([scenario_values]).T.reset_index()
        scenario_table.columns = ["field", "value"]
        scenario_table["value"] = scenario_table["value"].astype(str)
        st.dataframe(scenario_table, width="stretch", hide_index=True)
        st.download_button(
            "Download this prediction as CSV",
            data=current_scenario_frame().to_csv(index=False).encode("utf-8"),
            file_name="airalert_prediction.csv",
            mime="text/csv",
        )
        st.download_button(
            "Download this prediction as JSON",
            data=json.dumps(current_scenario_frame().iloc[0].to_dict(), indent=2).encode("utf-8"),
            file_name="airalert_prediction.json",
            mime="application/json",
        )
    with col2:
        st.plotly_chart(probability_chart(probabilities), width="stretch")

    st.info(
        "Interpretation: high traffic, high particulate matter, low wind and winter months usually increase risk. "
        "Green space and wind tend to reduce risk."
    )

elif page == "Model Evaluation":
    st.title("Model Evaluation")
    st.write(
        "The app uses a Random Forest classifier because it is robust for tabular data, fast enough "
        "for Streamlit and still explainable through feature importance."
    )

    col1, col2 = st.columns([0.8, 1.2])
    with col1:
        st.metric("Test accuracy", f"{model_bundle['accuracy']:.1%}")
        st.write("Confusion matrix labels: Low, Medium, High")
        st.dataframe(
            pd.DataFrame(
                model_bundle["confusion_matrix"],
                index=model_bundle["labels"],
                columns=model_bundle["labels"],
            ),
            width="stretch",
        )
    with col2:
        importance = feature_importance_table(model)
        st.plotly_chart(feature_importance_chart(importance), width="stretch")

    st.subheader("Classification report")
    report = pd.DataFrame(model_bundle["report"]).T
    st.dataframe(report, width="stretch")

elif page == "Sources & Export":
    st.title("Sources & Export")
    st.write(
        "This page makes the prototype transparent. The current version uses deterministic demo data "
        "so it runs reliably in PyCharm and Streamlit Cloud without API keys. The structure mirrors "
        "three real public-data layers."
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Cities", df["city"].nunique())
    col2.metric("Years", f"{df['year'].min()}-{df['year'].max()}")
    col3.metric("Dataset rows", f"{len(df):,}")

    st.subheader("Dataset layers used by the app")
    st.markdown(
        """
        - Air quality layer: PM2.5, PM10, NO2, O3 and AQI-like risk class.
        - Weather layer: temperature, humidity and wind speed.
        - City context layer: population, traffic, green space and industry indicators.
        """
    )

    st.subheader("Real public source mapping")
    st.markdown(
        """
        - OpenAQ-style measurements for PM2.5, PM10, NO2 and O3.
        - Open-Meteo-style weather history for temperature, humidity and wind.
        - World Cities / GeoNames-style metadata for coordinates and population.
        """
    )

    st.subheader("Why the app uses a deterministic operational dataset")
    st.write(
        "The classroom version keeps the data generation inside the repository so the app runs reliably during "
        "presentation and deployment without API keys, rate limits or broken downloads. The structure still "
        "represents three separate data layers and can be replaced by downloaded public CSV files in a later version."
    )

    st.download_button(
        "Download full generated dataset as CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="airalert_full_dataset.csv",
        mime="text/csv",
    )
    st.download_button(
        "Download current prediction as CSV",
        data=current_scenario_frame().to_csv(index=False).encode("utf-8"),
        file_name="airalert_current_prediction.csv",
        mime="text/csv",
    )

elif page == "QUA3CK Process":
    st.title("QUA3CK Process")
    st.write("This page translates AirAlert into the same course logic used by the example project.")

    with st.expander("Q - Question", expanded=True):
        st.write(
            "How can pollution, weather and city-context data be combined into a simple ML tool "
            "that predicts urban air-quality risk for non-expert users?"
        )
        st.write("Output of this phase: research question, target group, app goal and success criteria.")

    with st.expander("U - Understanding the Data", expanded=True):
        st.write(
            "The prototype studies three data layers: pollutant measurements, weather conditions "
            "and structural city indicators. The target variable is a Low/Medium/High risk class "
            "derived from an AQI-like score."
        )
        st.write("Output of this phase: data-layer description, feature groups, target variable and limitations.")

    with st.expander("A1 - Algorithm Selection"):
        st.write(
            "A Random Forest classifier was selected because it can model non-linear relationships "
            "and still provide feature importances for explanation."
        )
        st.write("Output of this phase: model family chosen for tabular classification.")

    with st.expander("A2 - Adapting Features"):
        st.write(
            "City names are encoded, monthly seasonality is included, and pollution/weather indicators "
            "are combined with city context."
        )
        st.write("Output of this phase: feature set for prediction and scenario sliders.")

    with st.expander("A3 - Adjusting Hyperparameters"):
        st.write(
            "The number of trees, tree depth and class balancing are adjusted to keep the model stable "
            "without making the app slow."
        )
        st.write("Output of this phase: stable model configuration for Streamlit.")

    with st.expander("C - Conclude"):
        st.write(
            "The model is evaluated with accuracy, a confusion matrix, a classification report and "
            "feature importance. Limitations are stated clearly so the output is not mistaken for "
            "official health advice."
        )
        st.write("Output of this phase: go/no-go justification for using the model in the app.")

    with st.expander("K - Knowledge Transfer"):
        st.write(
            "The Streamlit dashboard turns the model into an accessible tool with sliders, charts, "
            "risk labels and plain-language explanations."
        )
        st.write("Output of this phase: an interactive app that communicates the model result.")

    st.warning(
        "Disclaimer: This is a classroom ML prototype with deterministic demo data. It is not a medical "
        "or regulatory air-quality warning system."
    )
