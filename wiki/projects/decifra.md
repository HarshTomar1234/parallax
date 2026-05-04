---
title: Decifra
domain: projects
tags: mlops, fraud-detection, xai, zenml, mlflow, dvc, shap, lime, bentoml, xgboost
sources: [github-decifra, portfolio-projects]
last_updated: 2026-04-07
confidence: 0.95
links: [[mlops]], [[deep-learning]]
---

# Decifra

End-to-end MLOps fraud detection pipeline with explainable AI.

- **Repo:** https://github.com/HarshTomar1234/decifra
- **Demo:** https://huggingface.co/spaces/Coddieharsh/decifra-fraud-detection

---

## Performance

- **Precision-Recall AUC:** 88.52%
- **Pipeline complexity:** 9 interconnected execution steps
- **Primary Orchestrator:** ZenML

## 9-Step ZenML Pipeline

1. **Data Ingestion:** Securely loading raw transaction data.
2. **Data Validation:** Automated checks using `Great Expectations` to prevent data drift.
3. **Preprocessing:** Cleaning and normalizing data distributions.
4. **Feature Engineering:** Extracting high-signal temporal and numeric indicators.
5. **Model Training:** Ensembling XGBoost, LightGBM, and Random Forests.
6. **Evaluation:** Calculating robust PR-AUC and accuracy metrics.
7. **Model Selection:** Automatically promoting the highest scoring model variant.
8. **Explainability:** Attaching SHAP (global) and LIME (instance-level) diagnostics.
9. **Registration:** Committing the final model package directly into the `MLflow` registry.

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

## Core Tech Stack

- **ML Orchestration & Tooling:** ZenML, MLflow, DVC, BentoML
- **Modeling & XAI:** XGBoost, LightGBM, SHAP, LIME
- **Infrastructure:** Docker, GitHub Actions, Streamlit, Python

## Links

- [[mlops]] — pipeline tooling
- [[deep-learning]] — ensemble ML methods
