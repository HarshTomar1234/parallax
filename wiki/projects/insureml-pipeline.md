---
title: InsureML-Pipeline
domain: projects
tags: [MLOps, AWS, FastAPI, Docker]
sources: [https://github.com/HarshTomar1234/InsureML-Pipeline]
last_updated: 2026-04-07
confidence: 0.8
links: "[[mlops]], [[deep-learning]], [[connections]]"
---
# InsureML-Pipeline

## Project Overview

InsureML-Pipeline is an MLOps system for predicting vehicle insurance cross-sell opportunities. It uses machine learning to identify customers likely to purchase vehicle insurance, optimizing marketing and conversion rates.

Key outcomes:
*   87%+ model accuracy (Random Forest)
*   End-to-end automation from data ingestion to deployment
*   Cloud-native architecture on AWS
*   Real-time predictions via FastAPI REST API
*   Continuous training and deployment (CI/CD)
*   Production-ready code with robust logging and exception handling

## Key Features

### MLOps Best Practices
*   **Modular Architecture**: Separated components for ingestion, validation, transformation, training, evaluation, and deployment.
*   **Configuration Management**: YAML-based configuration for data schema and model parameters.
*   **Artifact Tracking**: Timestamped storage for experiment reproducibility.
*   **Model Versioning**: AWS S3-based model registry with version control.
*   **Data Validation**: Schema-based validation for data quality.
*   **Custom Exception Handling**: Robust error tracking and logging.
*   **Automated Testing**: Data quality checks and model performance validation.

### Production-Ready Capabilities
*   **FastAPI Web Application**: High-performance API with interactive documentation (Swagger UI).
*   **Docker Containerization**: Consistent deployment across environments.
*   **GitHub Actions CI/CD**: Automated testing, building, and deployment workflows.
*   **AWS Cloud Integration**: Utilizes S3, ECR, EC2 for scalable infrastructure.
*   **MongoDB Atlas**: Cloud-based NoSQL database for flexible data storage.
*   **Self-Hosted Runner**: EC2-based GitHub Actions runner for deployment automation.

### Data Processing Pipeline
*   **Data Ingestion**: Automated extraction from MongoDB Atlas.
*   **Feature Engineering**: Smart feature transformation and selection.
*   **Data Validation**: Comprehensive schema and quality checks.
*   **Imbalanced Data Handling**: SMOTE-based resampling techniques.
*   **Model Evaluation**: Automated model comparison and selection.
*   **Model Registry**: Version-controlled model storage in AWS S3.

## System Architecture

The MLOps system follows an end-to-end pipeline:

1.  **MongoDB Atlas**: Serves as the raw data storage.
2.  **Data Ingestion**: Fetches data from MongoDB, exports to a feature store, performs a 75-25 train-test split.
3.  **Data Validation**: Validates data against `schema.yaml`, checks column types, detects missing values, and generates a validation report.
4.  **Data Transformation**: Applies feature engineering, encodes categorical variables, scales numerical features, handles imbalanced data using SMOTE, and saves the preprocessing pipeline.
5.  **Model Training**: Trains a Random Forest Classifier with specified hyperparameters, performs cross-validation, and saves the trained model.
6.  **Model Evaluation**: Compares the newly trained model with the production model, calculates performance metrics, and makes an acceptance decision based on a 2% improvement threshold.
7.  **Model Pusher**: Pushes the accepted model to an AWS S3 bucket for model registry and version control.
8.  **FastAPI Application**: Provides REST API endpoints for real-time predictions, a web UI for data input, and a training trigger endpoint.
9.  **CI/CD Pipeline (GitHub Actions)**: Automates Docker image build, pushes to AWS ECR, and deploys to an EC2 instance.

## Technology Stack

### Core ML & Data Science
*   **Python 3.12**: Primary programming language.
*   **scikit-learn**: ML algorithms and preprocessing.
*   **pandas**: Data manipulation and analysis.
*   **NumPy**: Numerical computing.
*   **imbalanced-learn**: SMOTE for imbalanced datasets.
*   **Matplotlib & Seaborn, Plotly**: Data visualization.

### Web Framework & API
*   **FastAPI**: High-performance web framework.
*   **Uvicorn**: ASGI server.
*   **Jinja2**: Template engine.

### Database & Storage
*   **MongoDB Atlas**: Cloud-based NoSQL database.
*   **pymongo**: Python MongoDB driver.
*   **AWS S3**: Model registry and artifact storage.
*   **boto3**: AWS SDK for Python.

### DevOps & Deployment
*   **Docker**: Containerization.
*   **GitHub Actions**: CI/CD automation.
*   **AWS ECR**: Container registry.
*   **AWS EC2**: Application hosting.
*   **AWS IAM**: Access management.

### Configuration & Utilities
*   **PyYAML**: Configuration file parsing.
*   **dill**: Advanced Python serialization.

## Project Structure

*   `.github/workflows/`: CI/CD pipeline configuration (`aws.yaml`).
*   `artifact/`: Timestamped training artifacts (data_ingestion, data_validation, data_transformation, model_trainer).
*   `config/`: Model configuration (`model.yaml`) and data schema definition (`schema.yaml`).
*   `logs/`: Application logs.
*   `notebook/`: Sample dataset, EDA, and MongoDB integration demos.
*   `src/`: Core application logic.
    *   `cloud_storage/`: AWS S3 operations.
    *   `components/`: Individual ML pipeline stages (data_ingestion, data_validation, data_transformation, model_trainer, model_evaluation, model_pusher).
    *   `configuration/`: AWS and MongoDB connection setups.
    *   `constants/`: Project constants.
    *   `data_access/`: Data access layer for vehicle insurance data.
    *   `entity/`: Artifact, configuration, and estimator definitions.
    *   `exception/`: Custom exception handling.
    *   `logger/`: Logging configuration.
    *   `pipeline/`: End-to-end training and prediction pipelines.
    *   `utils/`: Utility functions.
*   `static/`: Web UI styling (`style.css`).
*   `templates/`: Web UI template (`vehicledata.html`).
*   `visuals/`: Project documentation images.
*   `app.py`: FastAPI application entry point.
*   `demo.py`: Testing script for the ML pipeline.
*   `Dockerfile`: Docker configuration.
*   `requirements.txt`: Python dependencies.

## ML Pipeline Components

### 1. Data Ingestion
*   **Input**: MongoDB collection (`vehicle-insurance-data`).
*   **Process**: Fetches data, exports to CSV files, splits into training (75%) and testing (25%) datasets.
*   **Output**: Train and test datasets stored in the artifact directory.

### 2. Data Validation
*   **Input**: Raw training and testing datasets.
*   **Process**: Validates data against `config/schema.yaml`, checks column data types, and detects missing values.
*   **Output**: A validation report (YAML format) indicating data quality status.

### 3. Data Transformation
*   **Input**: Validated training and testing datasets.
*   **Process**:
    *   Encodes categorical variables (Gender, Vehicle_Age, Vehicle_Damage).
    *   Scales numerical features (Age, Vintage, Annual_Premium).
    *   Handles imbalanced data using SMOTE.
    *   Constructs and saves a preprocessing pipeline.
*   **Output**: Transformed training and testing datasets, along with the saved preprocessing object.

### 4. Model Training
*   **Input**: Transformed training dataset.
*   **Algorithm**: Random Forest Classifier.
*   **Hyperparameters**: `n_estimators=200`, `min_samples_split=7`, `min_samples_leaf=6`, `max_depth=10`, `criterion=entropy`, `random_state=101`.
*   **Output**: A trained `model.pkl` file.

### 5. Model Evaluation
*   **Input**: Trained model, transformed testing dataset, and the current production model (if exists).
*   **Process**: Compares the new model's performance with the production model using metrics such as Accuracy, Precision, Recall, and F1-Score.
*   **Threshold**: Requires a 2% improvement in performance for the new model to be accepted.
*   **Output**: An evaluation report and an acceptance decision for the new model.

### 6. Model Pusher
*   **Input**: Accepted trained model.
*   **Process**: Uploads the accepted model to the AWS S3 model registry.
*   **Location**: `s3://insureml-pipeline-bucket/model-registry/`.
*   **Output**: A versioned model stored in AWS S3.

## API Endpoints

### `GET /`
*   **Purpose**: Renders the web interface for vehicle insurance prediction.
*   **Response**: HTML form for data input.

### `POST /`
*   **Purpose**: Predicts customer interest in vehicle insurance.
*   **Request Body**:
    ```json
    {
      "Gender": 1,
      "Age": 35,
      "Driving_License": 1,
      "Region_Code": 28.0,
      "Previously_Insured": 0,
      "Annual_Premium": 30000.0,
      "Policy_Sales_Channel": 152.0,
      "Vintage": 180,
      "Vehicle_Age_lt_1_Year": 0,
      "Vehicle_Age_gt_2_Years": 1,
      "Vehicle_Damage_Yes": 1
    }
    ```
*   **Response**:
    ```json
    {
      "context": "Response-Yes"
    }
    ```

### `GET /train`
*   **Purpose**: Initiates the complete ML training pipeline.
*   **Response**: `Training successful!!!` or an error message.

### `GET /docs`
*   **Purpose**: Provides interactive Swagger UI documentation for the API.

## Deployment

### AWS Infrastructure Setup

*   **MongoDB Atlas**: Configured with a cluster, database user, and network access (0.0.0.0/0). Connection string obtained.
*   **AWS IAM User**: `InsureML-Pipeline` user created with `AdministratorAccess` policy and access keys for CLI.
*   **AWS S3 Bucket**: `insureml-pipeline-bucket` created in `us-east-1` with "Block all public access" unchecked for model registry.
*   **AWS ECR Repository**: `vehicle_insurance_prediction_pipeline` created in `us-east-1` for Docker image storage.
*   **AWS EC2 Instance**: `vehicledata-machine` (Ubuntu Server 24.04 LTS, `t2.medium`) launched with a key pair (`insureml_pipeline.pem`) and a security group allowing HTTP (80), HTTPS (443), and Custom TCP (5000).
*   **EC2 Docker Setup**: Docker installed and configured on the EC2 instance.
*   **GitHub Self-Hosted Runner**: Configured on the EC2 instance as a service for GitHub Actions.

### CI/CD Pipeline (GitHub Actions)

The workflow (`.github/workflows/aws.yaml`) executes on pushes to the `main` branch.

**GitHub Secrets**:
*   `AWS_ACCESS_KEY_ID`
*   `AWS_SECRET_ACCESS_KEY`
*   `AWS_DEFAULT_REGION`
*   `ECR_REPO`
*   `MONGODB_URL`

**Workflow Stages**:
*   **Continuous-Integration**:
    *   Checks out code.
    *   Configures AWS credentials.
    *   Logs in to Amazon ECR.
    *   Builds Docker image.
    *   Pushes image to ECR.
*   **Continuous-Deployment**:
    *   Pulls the latest image from ECR.
    *   Stops any existing container.
    *   Runs the new container with environment variables.
    *   Verifies deployment.

## Configuration

### Schema Configuration (`config/schema.yaml`)

Defines the expected data schema for validation:
*   **columns**: `id`, `Gender`, `Age`, `Driving_License`, `Region_Code`, `Previously_Insured`, `Vehicle_Age`, `Vehicle_Damage`, `Annual_Premium`, `Policy_Sales_Channel`, `Vintage`, `Response`.
*   **numerical_columns**: `Age`, `Driving_License`, `Region_Code`, `Previously_Insured`, `Annual_Premium`, `Policy_Sales_Channel`, `Vintage`, `Response`.
*   **categorical_columns**: `Gender`, `Vehicle_Age`, `Vehicle_Damage`.
*   **num_features**: `Age`, `Vintage`.
*   **mm_columns**: `Annual_Premium`.

### Constants Configuration (`src/constants/__init__.py`)

Key parameters:
*   **Database**: `DATABASE_NAME="vehicle-insurance-domain"`, `COLLECTION_NAME="vehicle-insurance-data"`.
*   **Model Training**: `MODEL_TRAINER_N_ESTIMATORS=200`, `MODEL_TRAINER_MIN_SAMPLES_SPLIT=7`, `MODEL_TRAINER_MIN_SAMPLES_LEAF=6`, `MODEL_TRAINER_EXPECTED_SCORE=0.6`.
*   **Model Evaluation**: `MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE=0.02`.
*   **AWS**: `MODEL_BUCKET_NAME="insureml-pipeline-bucket"`, `MODEL_PUSHER_S3_KEY="model-registry"`, `REGION_NAME="us-east-1"`.
*   **Application**: `APP_HOST="0.0.0.0"`, `APP_PORT=5000`.

## Features Description

### Input Features
*   **Gender**: Binary (1: Male, 0: Female).
*   **Age**: Integer (customer age).
*   **Driving_License**: Binary (1: Has license, 0: No license).
*   **Region_Code**: Float (customer region).
*   **Previously_Insured**: Binary (1: Previously insured, 0: Not insured).
*   **Vehicle_Age**: Categorical (< 1 Year, 1-2 Year, > 2 Years).
*   **Vehicle_Damage**: Binary (1: Vehicle damaged, 0: No damage).
*   **Annual_Premium**: Float (annual premium amount).
*   **Policy_Sales_Channel**: Float (sales channel code).
*   **Vintage**: Integer (days associated with company).

### Target Variable
*   **Response**: Binary (1: Interested in vehicle insurance, 0: Not interested).

## Model Performance

The Random Forest Classifier achieves:
*   **Training Accuracy**: ~87%
*   **Test Accuracy**: ~85%
*   **Precision**: ~0.86
*   **Recall**: ~0.84
*   **F1-Score**: ~0.85

**Model Improvement Strategy**:
*   Automated model comparison with production model.
*   2% improvement threshold for model acceptance.
*   Continuous retraining with new data.

## Security Best Practices

*   **Environment Variables**: Sensitive credentials stored as environment variables.
*   **AWS IAM**: Least privilege access policies applied.
*   **MongoDB Atlas**: Network access restricted by IP address.
*   **Docker**: Non-root user execution within containers.
*   **GitHub Secrets**: Encrypted storage for credentials.
*   **S3 Bucket**: Versioning enabled for model artifacts.

## Troubleshooting

*   **MongoDB connection failed**: Verify `MONGODB_URL` environment variable and network access settings.
*   **AWS S3 access denied**: Confirm AWS credentials and IAM permissions.
*   **Docker container not starting**: Check container logs using `docker logs <container-id>`.
*   **Self-hosted runner offline**: Restart the runner service on EC2 (`sudo ./svc.sh restart`).
*   **Port 5000 already in use**: Change `APP_PORT` in constants or terminate the conflicting process.

## Testing

*   **Unit Tests**: Executed via `pytest tests/`.
*   **Integration Tests**:
    *   Training pipeline: `python demo.py`.
    *   Prediction pipeline: `curl -X POST http://localhost:5000/ -F "Gender=1" ...`.
*   **Model Validation**: Model loading from S3 verified programmatically.

## Monitoring & Logging

*   **Application Logs**: Stored in `logs/` directory with timestamped filenames (e.g., `logs/10_04_2025_01_28_58.log`).
*   **Log Format**: `[TIMESTAMP] - LEVEL - MODULE - LINE - MESSAGE`.
*   **Monitoring Endpoints**:
    *   Health check: `curl http://localhost:5000/`.
    *   Training status: `curl http://localhost:5000/train`.

## Learning Resources

This project showcases expertise in:
*   MLOps (end-to-end ML pipeline design).
*   Cloud Computing (AWS S3, ECR, EC2, IAM).
*   DevOps (Docker, CI/CD with GitHub Actions).
*   Web Development (FastAPI, REST APIs).
*   Database Management (MongoDB Atlas, NoSQL).
*   ML Engineering (feature engineering, model training, evaluation).
*   Software Engineering (modular design, OOP, exception handling).
*   Version Control (Git, GitHub).

## Contact

*   **GitHub Issues**: [https://github.com/HarshTomar1234/InsureML-Pipeline/issues](https://github.com/HarshTomar1234/InsureML-Pipeline/issues)

## Related

- [[mlops]] — end-to-end MLOps patterns this project implements
- [[deep-learning]] — ML fundamentals underlying the Random Forest pipeline
- [[connections]] — cross-domain synthesis of projects and skills