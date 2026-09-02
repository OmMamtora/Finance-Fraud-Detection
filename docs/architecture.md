# Architecture Overview

## High-Level Design

The system uses a layered architecture:

1. `data_ingestion` moves the raw data from the local project path into S3.
2. `data_processing` runs Spark ETL for scalable cleaning and transformation.
3. `feature_engineering` creates fraud-focused behavioral and transaction features.
4. `eda` profiles fraud distribution, missing values, and transaction amount behavior.
5. `model_training` trains multiple models and keeps the best recall-oriented model.
6. `model_evaluation` stores metrics for business and ML review.
7. `airflow_dags` automates the batch workflow.
8. `api_service` serves online predictions.
9. `dashboard` exposes fraud trends and model metrics.
10. `web_app` lets users manually submit transactions for scoring.

## Interview-Ready Explanation

This project starts by reading the raw financial transaction data from `Data/raw/financial_fraud_detection_dataset.csv` and uploading it into an S3-based data lake. A Spark ETL job cleans the data and writes standardized outputs back to S3 or local processed storage. A feature pipeline then creates domain-specific fraud features such as customer spending deviation, time between transactions, and merchant usage patterns.

After that, multiple machine learning models are trained and compared. Because fraud detection is highly imbalanced, the pipeline prioritizes recall and ROC-AUC instead of plain accuracy. The best model is saved as an artifact and can be uploaded to S3 for deployment.

Airflow automates the full batch flow. FastAPI exposes a `/predict` endpoint for real-time scoring, Streamlit shows fraud insights for analysts, and a simple web UI allows users to submit transaction details for fraud prediction.

## Deployment Summary

- `S3`: raw data, processed data, model artifacts
- `EC2` or `ECS`: API service, Streamlit dashboard, web app
- `MWAA` or self-managed Airflow: orchestration
- `CloudWatch`: logs and alerts
- `IAM`: secure access between services
