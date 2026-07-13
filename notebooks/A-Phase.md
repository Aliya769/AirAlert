# A-Phase: Algorithm, Adapting and Adjusting

This file defines how AirAlert's A3 phase should look, based on the Degrees of No Return reference project.

## A1 - Algorithm Selection

Compare several classifiers before choosing the final model:

- Logistic Regression as a simple baseline.
- Decision Tree as a readable tree model.
- Random Forest as the preferred final model.
- Gradient Boosting as a strong tabular alternative.

Use accuracy and macro F1-score. Macro F1 is important because Low, Medium and High risk should all matter.

## A2 - Adapting Features

Prepare the data for modeling:

- encode `city` with `OneHotEncoder`,
- pass numeric pollutant, weather and city-context features through,
- exclude `aqi_score` to avoid target leakage,
- use a scikit-learn `Pipeline` so preprocessing and prediction stay connected.

## A3 - Adjusting Hyperparameters

Tune the Random Forest:

- `n_estimators`,
- `max_depth`,
- `min_samples_leaf`,
- `class_weight`.

Use `GridSearchCV` with macro F1 scoring. The final goal is a stable Streamlit-ready model, not only the highest notebook score.

## Handoff to C-Phase

The C-phase should formally evaluate the chosen model with:

- accuracy,
- macro F1,
- confusion matrix,
- classification report,
- feature importance,
- qualitative decision matrix,
- limitations and go/no-go decision.
