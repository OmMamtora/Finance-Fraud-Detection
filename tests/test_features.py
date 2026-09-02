import pandas as pd

from feature_engineering.pipelines.build_features import build_features


def test_build_features_adds_expected_columns():
    df = pd.DataFrame(
        [
            {
                "customer_id": "c1",
                "merchant": "store_a",
                "amount": 100.0,
                "transaction_time": "2026-01-01 10:00:00",
            },
            {
                "customer_id": "c1",
                "merchant": "store_a",
                "amount": 120.0,
                "transaction_time": "2026-01-01 11:00:00",
            },
        ]
    )

    result = build_features(df)

    assert "transaction_hour" in result.columns
    assert "amount_deviation" in result.columns
    assert "seconds_since_last_txn" in result.columns

