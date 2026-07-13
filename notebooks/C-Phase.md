# C-Phase: Conclude and Evaluate

This document explains the Conclude phase of **AirAlert**. The C-phase checks whether the trained model is good enough for the project goal and communicates its strengths and limitations honestly.

---

## 1. Purpose of the C-Phase

The C-phase turns model training into a justified conclusion. A model should not be placed in a user-facing app only because it produces predictions. It must also be evaluated, interpreted and limited clearly.

For AirAlert, the conclusion question is:

**Is the Random Forest model stable and understandable enough to support a classroom Streamlit prototype for air-quality risk communication?**

---

## 2. Evaluation Method

The evaluation happens inside:

```text
src/modeling.py -> train_air_quality_model()
```

The dataset is split into:

- training data,
- test data.

The split uses:

```text
test_size = 0.25
random_state = 7
stratify = y
```

This means 25 percent of the data is held back for testing. Stratification keeps the Low, Medium and High class distribution consistent across train and test data.

---

## 3. Metrics Used

AirAlert reports several evaluation outputs:

- accuracy,
- confusion matrix,
- classification report,
- feature importance.

These metrics appear in the Streamlit page:

```text
Model Evaluation
```

The goal is not only to show one score, but to let the user understand how the model behaves.

---

## 4. Accuracy

Accuracy measures the share of correct predictions on the test set.

In the app, it is shown as:

```text
Test accuracy
```

Accuracy is useful because the target has three clear classes. However, accuracy alone is not enough. If one class is much more common than the others, a model could look strong while still performing badly on less frequent classes.

That is why the app also includes a confusion matrix and classification report.

---

## 5. Confusion Matrix

The confusion matrix compares true labels and predicted labels.

Labels:

```text
Low, Medium, High
```

It helps answer:

- Does the model confuse Medium and High?
- Are Low-risk cases predicted correctly?
- Is one class systematically over-predicted?

For a risk app, this matters because confusing High risk with Low risk would be more serious than a small numerical error.

---

## 6. Classification Report

The classification report includes:

- precision,
- recall,
- f1-score,
- support.

Meaning:

- precision checks how reliable a predicted class is,
- recall checks how many real cases of a class are found,
- f1-score balances precision and recall,
- support shows how many test examples belong to each class.

This gives a more detailed view than accuracy alone.

---

## 7. Feature Importance

Random Forest models provide feature importances. AirAlert displays the most important features in a chart.

This supports explainability because users can see which variables influence the model most. Important features may include pollutant values, wind, humidity, month or city-context indicators.

The purpose is not to prove causality. Feature importance shows how the trained model used the features in this dataset.

---

## 8. Interpretation of the Model

The model follows the logic built into the dataset:

- higher particulate matter increases risk,
- higher NO2 can increase risk,
- low wind can increase risk,
- winter months can increase particulate-related risk,
- city context can shift baseline risk.

The Streamlit app communicates this with:

- risk badge,
- trend chart,
- city comparison chart,
- probability chart,
- feature importance chart.

---

## 9. Limitations

The C-phase must state limitations clearly.

Important limitations:

- the dataset is deterministic demo data,
- the AQI-like score is simplified,
- the model is not trained on official live measurements,
- the app does not model street-level exposure,
- results are not medical or regulatory advice,
- real-world deployment would require validated public datasets.

These limitations are also mentioned in the app and documentation to prevent overclaiming.

---

## 10. Conclusion

The model is appropriate for the project goal because it:

- solves the defined classification task,
- runs quickly in Streamlit,
- produces interpretable probabilities,
- supports feature importance,
- fits the educational QUA3CK workflow,
- remains stable without external data dependencies.

The conclusion is therefore:

**AirAlert is suitable as a classroom ML prototype and deployed Streamlit dashboard, as long as its deterministic-data limitation is explained clearly.**

---

## 11. C-Phase Output

The output of the C-phase is:

- evaluated model,
- accuracy score,
- confusion matrix,
- classification report,
- feature-importance explanation,
- clear limitations,
- justified readiness for the K-phase.
