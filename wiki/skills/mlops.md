---
title: MLOps
domain: skills
tags: [mlops, mlflow, dvc, zenml, bentoml, docker, kubernetes, aws, prometheus, grafana, cicd]
sources: [github-profile, portfolio-projects, portfolio-more, resumes]
last_updated: 2026-04-07
confidence: 0.9
links: [deepguard, decifra, deep-learning]
---

# MLOps

End-to-end ML lifecycle management — from data versioning to production monitoring.

---

## Full Stack Mastered

### Orchestration
- **ZenML** — 9-step pipeline orchestration ([[decifra]])
- **GitHub Actions** — CI/CD automation ([[deepguard]], [[decifra]])

### Experiment Tracking
- **MLflow + DagsHub** — experiment logging, model registry, artifact storage
- Applied in: [[deepguard]] (Xception training), [[decifra]] (ensemble comparison)

### Data Versioning
- **DVC** — dataset versioning, pipeline caching, data lineage
- Applied in: [[deepguard]], [[decifra]]

### Model Serving
- **BentoML** — production API serving ([[decifra]])
- **FastAPI** — custom model APIs ([[ai-internship]], InsureML)
- **Streamlit / Gradio** — rapid ML demos

### Containerization & Deployment
- **Docker** — containerization of all production systems
- **AWS EKS** — Kubernetes orchestration ([[deepguard]])
- **AWS EC2, S3, Lambda** — compute, storage, serverless inference
- **AWS ECR** — container registry

### Monitoring & Observability
- **Prometheus** — metrics collection ([[deepguard]])
- **Grafana** — dashboards ([[deepguard]])
- **Great Expectations** — data validation ([[decifra]])

### Data Quality
- **Great Expectations** — schema validation, data drift detection ([[decifra]])

---

## Projects

| Project | Key Tools | Complexity |
|---------|-----------|-----------|
| [[deepguard]] | DVC + MLflow + Docker + AWS EKS + Prometheus/Grafana | Production cloud |
| [[decifra]] | ZenML + MLflow + DVC + BentoML + Great Expectations | Enterprise pipeline |
| InsureML Pipeline | MongoDB + AWS + FastAPI + Docker + GitHub Actions | Full-stack MLOps |
| MLOps Repo | 130+ commits covering entire domain | Learning deep dive |

---

## MLOps Learning Repo

- **Repo:** https://github.com/HarshTomar1234/MLOps-
- **Commits:** 130+
- Covers: Docker, Kubernetes, DVC, MLflow, CI/CD, Prometheus, Grafana
- Systematic documentation of every MLOps concept with hands-on implementations

---

## Links

- [[deepguard]] — full cloud MLOps pipeline
- [[decifra]] — ZenML orchestrated pipeline
- [[deep-learning]] — model training underpinning MLOps
