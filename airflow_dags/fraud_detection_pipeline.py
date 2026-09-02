from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from data_ingestion.scripts.local_to_s3 import upload_local_dataset_to_s3
from data_processing.jobs.spark_etl import run_spark_etl
from feature_engineering.pipelines.build_features import build_features
from model_training.trainers.train_models import train_models

import pandas as pd


def generate_features() -> None:
    source = "Data/raw/financial_fraud_detection_dataset.csv"
    target = "data/processed/transactions_features.csv"
    df = pd.read_csv(source)
    build_features(df).to_csv(target, index=False)


default_args = {
    "owner": "data-platform",
    "depends_on_past": False,
}


with DAG(
    dag_id="fraud_detection_batch_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["fraud", "ml", "spark"],
) as dag:
    ingest = PythonOperator(
        task_id="ingest_raw_data",
        python_callable=upload_local_dataset_to_s3,
        op_kwargs={
            "local_file": "Data/raw/financial_fraud_detection_dataset.csv",
            "s3_key": "raw/transactions/financial_fraud_detection_dataset.csv",
        },
    )

    process = PythonOperator(
        task_id="spark_etl",
        python_callable=run_spark_etl,
        op_kwargs={
            "input_path": "Data/raw/financial_fraud_detection_dataset.csv",
            "output_path": "data/processed/transactions_parquet",
        },
    )

    features = PythonOperator(task_id="feature_engineering", python_callable=generate_features)

    train = PythonOperator(
        task_id="train_model",
        python_callable=train_models,
        op_kwargs={
            "data_path": "data/processed/transactions_features.csv",
            "target_column": "is_fraud",
            "model_output_dir": "artifacts/models",
        },
    )

    ingest >> process >> features >> train
