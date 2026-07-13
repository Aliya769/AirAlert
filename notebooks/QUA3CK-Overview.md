# AirAlert QUA3CK Overview

This overview connects all phase documents for the AirAlert project.

## Phase Files

- `Q-Phase.md`: defines the problem, target users and main research question.
- `U-Phase.md`: explains the pollutant, weather and city-context data layers.
- `A-Phase.md`: explains algorithm selection, feature adaptation and model adjustment.
- `C-Phase.md`: evaluates the model and states limitations.
- `K-Phase.md`: explains Streamlit knowledge transfer and deployment.

## Short Project Logic

```text
pollution + weather + city context -> Random Forest classifier -> Low/Medium/High risk -> Streamlit dashboard
```

## Stability Decision

The deployed app should not depend on notebook execution. The Markdown phase files provide the full documentation for GitHub and presentation use, while `app.py` and the `src/` modules keep the Streamlit app running smoothly.
