---
title: InsureML-Pipeline
domain: projects
tags: [mlops, random-forest, smote, fastapi, docker, aws, mongodb, cicd, imbalanced-learning]
sources: [github-insureml-pipeline]
last_updated: 2026-05-05
confidence: 0.95
links: [mlops, deep-learning, connections]
---

# InsureML-Pipeline

Production-grade MLOps pipeline for vehicle insurance cross-sell prediction. Fully automated lifecycle — MongoDB ingestion through AWS EC2 deployment — with CI/CD via GitHub Actions.

- **Repo:** https://github.com/HarshTomar1234/InsureML-Pipeline

---

## Performance Metrics

| Metric | Value |
|--------|-------|
| Training accuracy | 87% |
| Test accuracy | 85% |
| Precision | 0.86 |
| Recall | 0.84 |
| F1-score | 0.85 |
| API response time | <100ms |
| CI/CD deploy time | <5 min |

---

## ML Pipeline

Seven modular, sequential stages with timestamped artifact storage:

| Stage | Detail |
|-------|--------|
| **Data Ingestion** | MongoDB Atlas → CSV export, 75/25 train-test split |
| **Data Validation** | Schema check against `config/schema.yaml` — column types, missing values |
| **Data Transformation** | Categorical encoding (Gender, Vehicle_Age, Vehicle_Damage), numerical scaling, SMOTE resampling, pipeline serialization via `dill` |
| **Model Training** | Random Forest Classifier (see hyperparams) |
| **Model Evaluation** | New model vs production baseline — accepts only if >2% improvement |
| **Model Pusher** | Accepted model → S3 model registry (`insureml-pipeline-bucket/model-registry/`) |
| **Serving** | FastAPI on port 5000 — `/` for predictions, `/train` to trigger retraining |

---

## Model

**Algorithm:** Random Forest Classifier

| Hyperparameter | Value |
|----------------|-------|
| n_estimators | 200 |
| max_depth | 10 |
| min_samples_split | 7 |
| min_samples_leaf | 6 |
| criterion | entropy |
| random_state | 101 |

**Class imbalance:** SMOTE resampling — the positive class (interested customers) is heavily underrepresented in cross-sell datasets; SMOTE synthesises minority samples before training.

---

## Dataset

Source: MongoDB Atlas, `vehicle-insurance-domain` database, `vehicle-insurance-data` collection.

**11 input features:**

| Category | Features |
|----------|---------|
| Demographic | Gender, Age, Driving_License |
| Geographic | Region_Code |
| Vehicle | Vehicle_Age (3-category), Vehicle_Damage (binary) |
| Policy | Previously_Insured, Annual_Premium, Policy_Sales_Channel, Vintage |

**Target:** `Response` — binary (1 = interested, 0 = not interested)

---

## Infrastructure

| Component | Detail |
|-----------|--------|
| Database | MongoDB Atlas (cloud NoSQL) |
| Model registry | AWS S3 — `insureml-pipeline-bucket`, `us-east-1` |
| Container registry | AWS ECR — `vehicle_insurance_prediction_pipeline` |
| Compute | AWS EC2 t2.medium, Ubuntu 24.04 LTS |
| CI/CD | GitHub Actions + self-hosted runner on EC2 |
| Serving | FastAPI + Uvicorn, Dockerized, port 5000 |

**CI/CD flow:** push to main → ECR image build + push → EC2 pulls image → old container stopped → new container started with env vars injected from GitHub Secrets.

---

## API

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Web UI for manual prediction input |
| `/` | POST | Submit 11-feature JSON, returns `Response-Yes` or `Response-No` |
| `/train` | GET | Triggers full retraining pipeline end-to-end |
| `/docs` | GET | Swagger auto-documentation |

---

## Core Tech Stack

- **ML:** Python 3.12, scikit-learn, imbalanced-learn (SMOTE), pandas, NumPy
- **Serving:** FastAPI, Uvicorn, Jinja2
- **Storage:** MongoDB Atlas (pymongo), AWS S3 (boto3), dill (pipeline serialization)
- **Infra:** Docker, AWS EC2 + ECR + S3 + IAM, GitHub Actions

---

## Links

- [[mlops]] — pipeline patterns, DVC, MLflow, monitoring
- [[deep-learning]] — ML foundations
- [[connections]] — cross-domain synthesis
