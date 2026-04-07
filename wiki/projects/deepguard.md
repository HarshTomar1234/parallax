---
title: DeepGuard
domain: projects
tags: mlops, deepfake, xception, dvc, mlflow, docker, aws, kubernetes, monitoring
sources: [github-deepguard, portfolio-projects]
last_updated: 2026-04-07
links: [[mlops]], [[deep-learning]], [[computer-vision]]
---

# DeepGuard

Production-grade MLOps pipeline for deepfake detection with complete ML lifecycle implementation.

- **Repo:** https://github.com/HarshTomar1234/DeepGuard-MLOps-Pipeline
- **Demo:** https://huggingface.co/spaces/Coddieharsh/DeepGuard

---

## Architecture

```
Data Ingestion
    → DVC versioning
    → Preprocessing pipeline
    → Xception transfer learning (GenImage dataset)
    → MLflow + DagsHub experiment tracking
    → Docker containerization
    → AWS EKS deployment
    → Prometheus + Grafana observability
    → CI/CD via GitHub Actions
```

## ML Pipeline

| Component | Detail |
|-----------|--------|
| **Model** | Xception (transfer learning) |
| **Dataset** | GenImage deepfake dataset |
| **Data versioning** | DVC |
| **Experiment tracking** | MLflow + DagsHub |
| **Deployment** | Docker + AWS EKS |
| **Monitoring** | Prometheus + Grafana |
| **CI/CD** | GitHub Actions |

## Key Differentiators

- End-to-end MLOps — not just training, but full production lifecycle
- Containerized with Docker, orchestrated on Kubernetes (EKS)
- Observability stack included at deployment time
- Automated triggers for data → training → evaluation → deployment

## Tech Stack

```
Python | PyTorch | Xception | DVC | MLflow | DagsHub | Docker | AWS EKS | Prometheus | Grafana | GitHub Actions
```

## Links

- [[mlops]] — domain page
- [[deep-learning]] — model architecture
- [[computer-vision]] — vision model
