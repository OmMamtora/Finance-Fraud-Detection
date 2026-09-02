# from fastapi import APIRouter

# from api_service.app.schemas import PredictionResponse, TransactionRequest
# from api_service.app.services.inference import FraudInferenceService


# router = APIRouter()
# service = FraudInferenceService()


# @router.post("/predict", response_model=PredictionResponse)
# def predict(request: TransactionRequest) -> PredictionResponse:
#     result = service.predict(request.model_dump())
#     return PredictionResponse(**result)


# from fastapi import APIRouter
# from api_service.app.schemas import PredictionResponse, TransactionRequest
# from api_service.app.services.inference import FraudInferenceService

# router = APIRouter()

# service = FraudInferenceService()  # ✅ create instance

# @router.post("/predict", response_model=PredictionResponse)
# def predict(request: TransactionRequest):   # ✅ NO self here
#     result = service.predict(request.model_dump())
#     return PredictionResponse(**result)


from fastapi import APIRouter
from api_service.app.schemas import PredictionResponse, TransactionRequest
from api_service.app.services.inference import FraudInferenceService

router = APIRouter()
service = FraudInferenceService()

@router.post("/predict", response_model=PredictionResponse)
def predict(request: TransactionRequest):
    result = service.predict(request.model_dump())
    return PredictionResponse(**result)