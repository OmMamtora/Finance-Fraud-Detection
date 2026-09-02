import pandas as pd

from config.settings import settings
from utils.common import load_model


# ======================================
# DEFAULT PAYLOAD
# ======================================

DEFAULT_INFERENCE_PAYLOAD = {

    "sender_account": "ACC000001",
    "receiver_account": "ACC000002",

    "amount": 1000.0,

    "transaction_type": "payment",
    "merchant_category": "utilities",

    "location": "pune",

    "device_used": "mobile",

    "time_since_last_transaction": 60.0,

    "payment_channel": "upi",

    "transaction_hour": 12,
    "transaction_dayofweek": 0,

    "customer_avg_amount": 1000.0,

    "merchant_frequency": 1,
}


# ======================================
# FRAUD INFERENCE SERVICE
# ======================================

class FraudInferenceService:

    def __init__(self):

        print("\n🚀 Loading Fraud Detection Model...")

        self.pipeline = load_model(
            "artifacts/models/final_stacking_model.joblib"
        )

        self.model_version = "v4"

        print("✅ Model Loaded Successfully")

    # ======================================
    # BUILD FEATURE FRAME
    # ======================================

    def _build_feature_frame(
        self,
        payload: dict
    ) -> pd.DataFrame:

        # ======================================
        # MERGE PAYLOAD
        # ======================================

        normalized = DEFAULT_INFERENCE_PAYLOAD.copy()

        normalized.update(payload)

        # ======================================
        # BASIC VALUES
        # ======================================

        amount = float(
            normalized["amount"]
        )

        customer_avg = float(
            normalized.get(
                "customer_avg_amount",
                1000
            )
        )

        txn_hour = int(
            normalized.get(
                "transaction_hour",
                12
            )
        )

        mins_since_txn = float(
            normalized.get(
                "time_since_last_transaction",
                60
            )
        )

        merchant_frequency = float(
            normalized.get(
                "merchant_frequency",
                1
            )
        )

        transaction_type = str(
            normalized.get(
                "transaction_type",
                ""
            )
        ).lower()

        location = str(
            normalized.get(
                "location",
                ""
            )
        ).lower()

        device = str(
            normalized.get(
                "device_used",
                ""
            )
        ).lower()

        payment_channel = str(
            normalized.get(
                "payment_channel",
                ""
            )
        ).lower()

        # ======================================
        # NIGHT TRANSACTION
        # ======================================

        normalized["is_night_transaction"] = int(

            txn_hour in [0, 1, 2, 3, 4, 23]

        )

        # ======================================
        # DYNAMIC AVG AMOUNT
        # ======================================

        dynamic_avg = max(

            amount * 0.15,
            500

        )

        avg_amount = max(

            customer_avg,
            dynamic_avg

        )

        # ======================================
        # AMOUNT FEATURES
        # ======================================

        normalized["amount_ratio"] = (

            amount / avg_amount

        )

        normalized["amount_deviation"] = (

            amount - avg_amount

        )

        normalized["spending_deviation_score"] = (

            amount / avg_amount

        )

        # ======================================
        # TIME FEATURES
        # ======================================

        normalized["seconds_since_last_txn"] = (

            mins_since_txn * 60

        )

        # ======================================
        # VELOCITY SCORE
        # ======================================

        velocity_score = 0

        # Fast repeated transactions
        if mins_since_txn < 1:
            velocity_score += 8

        elif mins_since_txn < 5:
            velocity_score += 5

        elif mins_since_txn < 30:
            velocity_score += 2

        # Merchant frequency
        velocity_score += min(
            merchant_frequency,
            10
        )

        # Large amount
        if amount > 50000:
            velocity_score += 5

        if amount > 200000:
            velocity_score += 5

        # Risky transaction type
        if transaction_type in [
            "withdrawal",
            "cash_out"
        ]:
            velocity_score += 3

        normalized["velocity_score"] = velocity_score

        # ======================================
        # HIGH VELOCITY FLAG
        # ======================================

        normalized["high_velocity_flag"] = int(

            velocity_score >= 10

        )

        # ======================================
        # GEO ANOMALY SCORE
        # ======================================

        geo_score = 0.15

        high_risk_locations = [

            "foreign",
            "unknown",
            "international"

        ]

        # Foreign alone ≠ fraud
        if location in high_risk_locations:
            geo_score += 0.25

        # Night transactions
        if normalized["is_night_transaction"]:
            geo_score += 0.15

        # Large amount
        if amount > 50000:
            geo_score += 0.15

        if amount > 200000:
            geo_score += 0.10

        # Risky device
        if device in [
            "atm",
            "pos"
        ]:
            geo_score += 0.10

        # Risky payment channel
        if payment_channel in [
            "wallet",
            "crypto"
        ]:
            geo_score += 0.10

        # Velocity effect
        if velocity_score >= 10:
            geo_score += 0.15

        # Spending anomaly
        if normalized[
            "spending_deviation_score"
        ] >= 3:

            geo_score += 0.10

        geo_score = min(
            geo_score,
            1.0
        )

        normalized["geo_anomaly_score"] = geo_score

        # ======================================
        # HIGH GEO FLAG
        # ======================================

        normalized["high_geo_anomaly_flag"] = int(

            geo_score >= 0.8

        )

        # ======================================
        # CREATE DATAFRAME
        # ======================================

        df = pd.DataFrame([normalized])

        # ======================================
        # DEBUG LOGS
        # ======================================

        print("\n📊 FINAL INPUT DATA:")
        print(df)

        print("\n📊 FINAL COLUMNS:")
        print(df.columns.tolist())

        print("\n📊 SHAPE:")
        print(df.shape)

        return df

    # ======================================
    # PREDICT
    # ======================================

    def predict(
        self,
        payload: dict
    ) -> dict:

        try:

            # ======================================
            # BUILD FEATURES
            # ======================================

            features = self._build_feature_frame(
                payload
            )

            # ======================================
            # MODEL PREDICTION
            # ======================================

            probabilities = self.pipeline.predict_proba(
                features
            )[0]

            probability = float(
                probabilities[1]
            )

            print("\nRAW PROBABILITIES:")
            print(probabilities)

            print("\n🎯 BASE FRAUD PROBABILITY:")
            print(probability)

            # ======================================
            # EXTRACT FEATURES
            # ======================================

            velocity_score = features[
                "velocity_score"
            ].iloc[0]

            geo_score = features[
                "geo_anomaly_score"
            ].iloc[0]

            amount = features[
                "amount"
            ].iloc[0]

            device = str(
                features[
                    "device_used"
                ].iloc[0]
            ).lower()

            payment_channel = str(
                features[
                    "payment_channel"
                ].iloc[0]
            ).lower()

            is_night = int(
                features[
                    "is_night_transaction"
                ].iloc[0]
            )

            # ======================================
            # RISK BOOST ENGINE
            # ======================================

            risk_boost = 0

            # Large amount
            if amount > 100000:
                risk_boost += 0.08

            if amount > 300000:
                risk_boost += 0.10

            # Velocity
            if velocity_score >= 10:
                risk_boost += 0.10

            if velocity_score >= 18:
                risk_boost += 0.10

            # Geo anomaly
            if geo_score >= 0.5:
                risk_boost += 0.08

            if geo_score >= 0.8:
                risk_boost += 0.10

            # Night transaction
            if is_night:
                risk_boost += 0.08

            # Risky payment
            if payment_channel in [
                "wallet",
                "crypto"
            ]:
                risk_boost += 0.05

            # ATM/POS
            if device in [
                "atm",
                "pos"
            ]:
                risk_boost += 0.05

            # ======================================
            # FINAL PROBABILITY
            # ======================================

            probability = min(
                probability + risk_boost,
                0.98
            )

            fraud_percentage = round(
                probability * 100,
                2
            )

            print("\n🔥 FINAL FRAUD %:")
            print(fraud_percentage)

            # ======================================
            # FINAL DECISION
            # ======================================

            is_fraud = probability >= 0.5

            return {

                "fraud_probability":
                    fraud_percentage,

                "is_fraud":
                    bool(is_fraud),

                "risk_level":
                    (
                        "HIGH"
                        if fraud_percentage >= 70
                        else
                        "MEDIUM"
                        if fraud_percentage >= 40
                        else
                        "LOW"
                    ),

                "model_version":
                    self.model_version
            }

        except Exception as e:

            import traceback

            print("\n❌ PREDICTION ERROR")
            traceback.print_exc()

            raise e