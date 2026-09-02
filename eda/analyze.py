from pathlib import Path

import pandas as pd

from utils.logger import get_logger


logger = get_logger(__name__)


def run_eda(data_path: str) -> dict:
    df = pd.read_csv(data_path)
    insights = {
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "missing_values": df.isna().sum().to_dict(),
    }

    if "is_fraud" in df.columns:
        insights["fraud_distribution"] = df["is_fraud"].value_counts(dropna=False).to_dict()

    if "amount" in df.columns:
        insights["amount_summary"] = df["amount"].describe().to_dict()

    output = Path("artifacts/reports/eda_summary.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(pd.Series(insights).to_json(indent=2), encoding="utf-8")
    logger.info("EDA summary written to %s", output)
    return insights


if __name__ == "__main__":
    run_eda("Data/processed/transactions_features.csv")
