from __future__ import annotations

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


FEATURES = [
    "city",
    "month",
    "population_m",
    "traffic_index",
    "green_space_index",
    "industrial_index",
    "temperature_c",
    "humidity_pct",
    "wind_kmh",
    "pm25",
    "pm10",
    "no2",
    "o3",
]


def train_air_quality_model(df: pd.DataFrame) -> dict[str, object]:
    x = df[FEATURES]
    y = df["risk_level"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=7, stratify=y
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("city", OneHotEncoder(handle_unknown="ignore"), ["city"]),
            ("num", "passthrough", [col for col in FEATURES if col != "city"]),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=160,
                    max_depth=8,
                    min_samples_leaf=3,
                    random_state=7,
                    class_weight="balanced",
                ),
            ),
        ]
    )
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    return {
        "model": model,
        "accuracy": accuracy_score(y_test, predictions),
        "confusion_matrix": confusion_matrix(y_test, predictions, labels=["Low", "Medium", "High"]),
        "report": classification_report(y_test, predictions, output_dict=True, zero_division=0),
        "labels": ["Low", "Medium", "High"],
    }


def predict_risk(model: Pipeline, values: dict[str, object]) -> tuple[str, dict[str, float]]:
    row = pd.DataFrame([values])[FEATURES]
    prediction = str(model.predict(row)[0])
    probabilities = model.predict_proba(row)[0]
    classes = list(model.classes_)
    return prediction, {classes[i]: float(probabilities[i]) for i in range(len(classes))}


def feature_importance_table(model: Pipeline) -> pd.DataFrame:
    pre = model.named_steps["preprocessor"]
    clf = model.named_steps["classifier"]
    feature_names = list(pre.get_feature_names_out())
    clean_names = [name.replace("num__", "").replace("city__city_", "City: ") for name in feature_names]
    table = pd.DataFrame({"feature": clean_names, "importance": clf.feature_importances_})
    return table.sort_values("importance", ascending=False).head(12)
