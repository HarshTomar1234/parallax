---
title: Decifra
domain: projects
tags: mlops, fraud-detection, xai, zenml, mlflow, dvc, shap, lime, bentoml, xgboost
sources: [github-decifra, portfolio-projects]
last_updated: 2026-04-07
links: [[mlops]], [[deep-learning]]
---

# Decifra

End-to-end MLOps fraud detection pipeline with explainable AI.

- **Repo:** https://github.com/HarshTomar1234/decifra
- **Demo:** https://huggingface.co/spaces/Coddieharsh/decifra-fraud-detection

---

## Performance

```
PR-AUC: 88.52%
Pipeline steps: 9
Orchestrator: ZenML
```

## 9-Step ZenML Pipeline

```
1. Data Ingestion
2. Data Validation (Great Expectations)
3. Preprocessing
4. Feature Engineering
5. Model Training  (XGBoost + LightGBM + Random Forest ensemble)
6. Evaluation
7. Model Selection
8. Explainability  (SHAP global + LIME instance-level)
9. Registration    (MLflow model registry)
```

## ML Stack

| Component | Tool |
|-----------|------|
| Orchestration | ZenML |
| Models | XGBoost + LightGBM + Random Forest ensemble |
| Hyperparameter optimization | Optuna |
| Class imbalance | SMOTE |
| Experiment tracking | MLflow |
| Data versioning | DVC |
| Model serving | BentoML |
| Data validation | Great Expectations |
| Explainability | SHAP (global) + LIME (instance-level) |
| UI | Streamlit dashboard |

## Explainability Approach

- **SHAP:** Global feature importance — which features drive fraud across dataset
- **LIME:** Instance-level — why a specific transaction was flagged
- Every prediction includes confidence + feature contribution breakdown
- Clinical-style report output

## Tech Stack

```
Python | ZenML | XGBoost | LightGBM | SHAP | LIME | MLflow | DVC | BentoML | Docker | GitHub Actions | Streamlit
```

## Links

- [[mlops]] — pipeline tooling
- [[deep-learning]] — ensemble ML methods
