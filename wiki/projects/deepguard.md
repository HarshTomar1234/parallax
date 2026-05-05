---
title: DeepGuard
domain: projects
tags: mlops, deepfake, xception, dvc, mlflow, docker, aws, kubernetes, monitoring
sources: [github-deepguard, portfolio-projects]
last_updated: 2026-04-07
confidence: 0.95
links: "[[mlops]], [[deep-learning]], [[computer-vision]]"
---

# DeepGuard

Production-grade MLOps pipeline for deepfake detection with complete ML lifecycle implementation.

- **Repo:** https://github.com/HarshTomar1234/DeepGuard-MLOps-Pipeline
- **Demo:** https://huggingface.co/spaces/Coddieharsh/DeepGuard

---

## Architecture

**Workflow Execution:**
1. **Data Ingestion:** Tracked securely via DVC versioning.
2. **Preprocessing:** Standardized image transformation pipelines.
3. **Training Engine:** Xception transfer learning model trained on the GenImage dataset.
4. **Experiment Tracking:** Logging natively to MLflow and DagsHub.
5. **Infrastructure:** Model instances grouped via Docker containerization and orchestrated on AWS EKS.
6. **Observability:** Prometheus + Grafana telemetry dashboard integration.
7. **Automation:** Fully triggered CI/CD through GitHub Actions.

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

## Core Tech Stack

- **Model Ecosystem:** Python, PyTorch, Xception Architecture
- **MLOps & Tracking:** DVC, MLflow, DagsHub
- **Platform & Infrastructure:** Docker, AWS EKS, Prometheus, Grafana, GitHub Actions

## Links

- [[mlops]] — domain page
- [[deep-learning]] — model architecture
- [[computer-vision]] — vision model
