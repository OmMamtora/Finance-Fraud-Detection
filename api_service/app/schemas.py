from pydantic import BaseModel, Field


class TransactionRequest(BaseModel):
    amount: float = Field(..., gt=0)
    sender_account: str
    receiver_account: str
    transaction_type: str
    merchant_category: str
    location: str
    device_used: str
    payment_channel: str
    transaction_hour: int = Field(..., ge=0, le=23)
    transaction_dayofweek: int = Field(..., ge=0, le=6)
    is_night_transaction: int = Field(0, ge=0, le=1)
    customer_avg_amount: float = 0
    amount_deviation: float = 0
    seconds_since_last_txn: float = 0
    merchant_frequency: int = 1
    time_since_last_transaction: float = 0
    spending_deviation_score: float = 0
    velocity_score: int = 0
    geo_anomaly_score: float = 0
    high_velocity_flag: int = Field(0, ge=0, le=1)
    high_geo_anomaly_flag: int = Field(0, ge=0, le=1)


class PredictionResponse(BaseModel):
    fraud_probability: float
    is_fraud: bool
    model_version: str
