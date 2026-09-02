import pandas as pd

from utils.logger import get_logger


logger = get_logger(__name__)


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()

    if "timestamp" in data.columns:
        data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
        data["transaction_hour"] = data["timestamp"].dt.hour.fillna(0).astype(int)
        data["transaction_dayofweek"] = data["timestamp"].dt.dayofweek.fillna(0).astype(int)
        data["is_night_transaction"] = data["transaction_hour"].isin([0, 1, 2, 3, 4, 23]).astype(int)

    if {"sender_account", "amount"}.issubset(data.columns):
        data["customer_avg_amount"] = data.groupby("sender_account")["amount"].transform("mean")
        data["amount_deviation"] = data["amount"] - data["customer_avg_amount"]

    if "time_since_last_transaction" in data.columns:
        data["seconds_since_last_txn"] = data["time_since_last_transaction"].fillna(0)

    if {"sender_account", "merchant_category"}.issubset(data.columns):
        data["merchant_frequency"] = (
            data.groupby(["sender_account", "merchant_category"])["merchant_category"].transform("count")
        )

    if "velocity_score" in data.columns:
        data["high_velocity_flag"] = (data["velocity_score"] >= data["velocity_score"].median()).astype(int)

    if "geo_anomaly_score" in data.columns:
        data["high_geo_anomaly_flag"] = (
            data["geo_anomaly_score"] >= data["geo_anomaly_score"].median()
        ).astype(int)

    logger.info("Feature engineering completed with %s columns", len(data.columns))
    return data


if __name__ == "__main__":
    source = "Data/raw/financial_fraud_detection_dataset.csv"
    target = "Data/processed/transactions_features.csv"
    dataset = pd.read_csv(source)
    build_features(dataset).to_csv(target, index=False)
