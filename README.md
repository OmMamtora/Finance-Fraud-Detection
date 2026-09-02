# End-to-End Fraud Detection System using Big Data and Machine Learning

This project is a production-style starter template for a scalable fraud detection platform. It covers data ingestion, Spark-based processing, feature engineering, model training and evaluation, workflow orchestration with Airflow, a FastAPI prediction service, a Streamlit dashboard, and a lightweight web app.

The raw input dataset for this project is expected at `D:\Finance-Fraud-Detection-\Data\raw\financial_fraud_detection_dataset.csv`, and the ingestion layer uploads that local file into Amazon S3.

## Project Structure

```text
Finance-Fraud-Detection-/
|-- README.md
|-- requirements.txt
|-- config/
|   |-- app_config.yaml
|   |-- aws_config.yaml
|   |-- logging_config.yaml
|   `-- settings.py
|-- data/
|   |-- external/
|   |-- processed/
|   `-- raw/
|-- data_ingestion/
|   `-- scripts/
|       `-- local_to_s3.py
|-- data_processing/
|   `-- jobs/
|       `-- spark_etl.py
|-- feature_engineering/
|   `-- pipelines/
|       `-- build_features.py
|-- model_training/
|   `-- trainers/
|       `-- train_models.py
|-- model_evaluation/
|   |-- evaluate.py
|   `-- reports/
|-- airflow_dags/
|   `-- fraud_detection_pipeline.py
|-- api_service/
|   `-- app/
|       |-- main.py
|       |-- schemas.py
|       |-- routers/
|       |   `-- predict.py
|       `-- services/
|           `-- inference.py
|-- dashboard/
|   `-- streamlit_app.py
|-- web_app/
|   |-- app.py
|   `-- templates/
|       `-- index.html
|-- utils/
|   |-- common.py
|   |-- logger.py
|   `-- s3.py
|-- logs/
|-- artifacts/
|   |-- features/
|   |-- models/
|   `-- reports/
|-- docs/
|   `-- architecture.md
|-- eda/
|   `-- analyze.py
`-- tests/
    |-- test_api.py
    `-- test_features.py
```

## End-to-End Flow

1. Read the raw transaction dataset from the local path `Data/raw/financial_fraud_detection_dataset.csv` and upload it to Amazon S3.
2. Run Apache Spark ETL jobs to clean, standardize, and save processed data.
3. Build fraud-specific features such as velocity, amount deviation, and customer behavior signals.
4. Perform EDA to understand fraud patterns, imbalance, and behavioral anomalies.
5. Train fraud models like Logistic Regression, Random Forest, and XGBoost.
6. Evaluate models using recall-focused metrics and store the best artifact.
7. Save trained model files to S3 for deployment and versioning.
8. Orchestrate the full workflow using Apache Airflow.
9. Serve predictions through a FastAPI endpoint.
10. Show business metrics through a Streamlit dashboard.
11. Provide a simple web interface for manual fraud prediction.

## Why This Design Works

- Modular: each layer has a single responsibility.
- Scalable: Spark handles large data and S3 acts as a data lake.
- Production-friendly: config, logging, tests, and reusable utilities are separated.
- Interview-ready: the flow is easy to explain from ingestion to deployment.

## Data Ingestion Source

The project now uses a local raw dataset instead of pulling directly from Kaggle during execution.

- Local source file: `Data/raw/financial_fraud_detection_dataset.csv`
- S3 destination key: `raw/transactions/financial_fraud_detection_dataset.csv`
- Upload script: `python data_ingestion/scripts/local_to_s3.py`
- Spark ETL input: `Data/raw/financial_fraud_detection_dataset.csv`
- Feature engineering input: `Data/raw/financial_fraud_detection_dataset.csv`

## Quick Start

```bash
pip install -r requirements.txt
uvicorn api_service.app.main:app --reload
streamlit run dashboard/streamlit_app.py
python web_app/app.py
```

## Suggested Improvements

- Add Kafka and Spark Structured Streaming for real-time fraud scoring.
- Add model monitoring for drift, latency, and recall degradation.
- Add CI/CD with GitHub Actions and containerized deployment.
- Register models using MLflow or SageMaker Model Registry.
- Add feature store support for online and offline consistency.
