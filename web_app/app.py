from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api_service.app.services.inference import FraudInferenceService


app = FastAPI(title="Fraud Detection Web App")
app.mount("/static", StaticFiles(directory="web_app/static"), name="static")
templates = Jinja2Templates(directory="web_app/templates")
service = FraudInferenceService()


def build_page_context(result=None, payload=None, risk_label=None, risk_tone="neutral"):
    payload = payload or {}
    probability = float(result["fraud_probability"]) if result else 0.0
    confidence_label = "High Confidence" if probability >= 0.75 or probability <= 0.2 else "Moderate Confidence"
    active_section = "Transaction Scoring"

    signals = [
        {
            "label": "Late Night Activity",
            "value": "Active" if int(payload.get("transaction_hour", 0)) in [0, 1, 2, 3, 4, 23] else "Normal",
            "tone": "warning" if int(payload.get("transaction_hour", 0)) in [0, 1, 2, 3, 4, 23] else "safe",
        },
        {
            "label": "Velocity Pressure",
            "value": f"{int(payload.get('velocity_score', 0))}",
            "tone": "critical" if int(payload.get("velocity_score", 0)) >= 15 else "warning" if int(payload.get("velocity_score", 0)) >= 8 else "safe",
        },
        {
            "label": "Geo Anomaly",
            "value": f"{float(payload.get('geo_anomaly_score', 0)):.2f}",
            "tone": "critical" if float(payload.get("geo_anomaly_score", 0)) >= 0.85 else "warning" if float(payload.get("geo_anomaly_score", 0)) >= 0.5 else "safe",
        },
        {
            "label": "Spend Deviation",
            "value": f"{float(payload.get('spending_deviation_score', 0)):.2f}",
            "tone": "warning" if float(payload.get("spending_deviation_score", 0)) >= 2 else "safe",
        },
    ]

    if probability >= 0.75:
        analyst_actions = [
            "Trigger step-up authentication before settlement.",
            "Route transaction to manual review queue immediately.",
            "Temporarily restrict beneficiary and monitor linked devices.",
        ]
    elif probability >= 0.5:
        analyst_actions = [
            "Hold for secondary verification if user behavior looks unusual.",
            "Cross-check device and location changes against recent history.",
            "Increase monitoring on next 24 hours of customer activity.",
        ]
    else:
        analyst_actions = [
            "Allow transaction and continue passive monitoring.",
            "Track repeated attempts from the same sender and device.",
            "Use this response as baseline behavior for future scoring.",
        ]

    recent_alerts = [
        {"title": "Cross-Border Burst", "meta": "4 linked accounts flagged in the last 18 min", "tone": "critical"},
        {"title": "Device Fingerprint Drift", "meta": "New browser and IP pattern detected", "tone": "warning"},
        {"title": "Merchant Spike Watch", "meta": "Utility payments stable across monitored cohort", "tone": "safe"},
    ]

    nav_sections = [
        {"label": "Executive Overview", "meta": "Business KPIs and fraud posture", "icon": "01", "active": False},
        {"label": "Transaction Scoring", "meta": "Live decision engine", "icon": "02", "active": True},
        {"label": "Case Management", "meta": "Analyst queues and escalations", "icon": "03", "active": False},
        {"label": "Model Monitoring", "meta": "Drift, recall, and threshold health", "icon": "04", "active": False},
        {"label": "Data Pipeline", "meta": "S3, Spark, features, orchestration", "icon": "05", "active": False},
        {"label": "Access Control", "meta": "Audit trails and governance", "icon": "06", "active": False},
    ]

    top_nav = ["Overview", "Detection", "Investigations", "Models", "DataOps", "Settings"]

    return {
        "result": result,
        "risk_label": risk_label,
        "risk_tone": risk_tone,
        "confidence_label": confidence_label,
        "active_section": active_section,
        "signals": signals,
        "analyst_actions": analyst_actions,
        "recent_alerts": recent_alerts,
        "nav_sections": nav_sections,
        "top_nav": top_nav,
        "payload": payload,
    }


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    context = build_page_context()
    context["request"] = request
    return templates.TemplateResponse("index.html", context)


@app.post("/score", response_class=HTMLResponse)
def score(
    request: Request,
    amount: float = Form(...),
    sender_account: str = Form(...),
    receiver_account: str = Form(...),
    transaction_type: str = Form(...),
    merchant_category: str = Form(...),
    location: str = Form(...),
    device_used: str = Form(...),
    payment_channel: str = Form(...),
    transaction_hour: int = Form(...),
    transaction_dayofweek: int = Form(...),
    time_since_last_transaction: float = Form(0),
    spending_deviation_score: float = Form(0),
    velocity_score: int = Form(0),
    geo_anomaly_score: float = Form(0),
):
    payload = {
        "amount": amount,
        "sender_account": sender_account,
        "receiver_account": receiver_account,
        "transaction_type": transaction_type,
        "merchant_category": merchant_category,
        "location": location,
        "device_used": device_used,
        "payment_channel": payment_channel,
        "transaction_hour": transaction_hour,
        "transaction_dayofweek": transaction_dayofweek,
        "time_since_last_transaction": time_since_last_transaction,
        "spending_deviation_score": spending_deviation_score,
        "velocity_score": velocity_score,
        "geo_anomaly_score": geo_anomaly_score,
        "customer_avg_amount": amount,
        "merchant_frequency": 1,
    }
    result = service.predict(payload)
    probability = float(result["fraud_probability"])
    if probability >= 0.75:
        risk_label = "Critical Risk"
        risk_tone = "critical"
    elif probability >= 0.5:
        risk_label = "Elevated Risk"
        risk_tone = "warning"
    else:
        risk_label = "Low Risk"
        risk_tone = "safe"

    context = build_page_context(result=result, payload=payload, risk_label=risk_label, risk_tone=risk_tone)
    context["request"] = request
    return templates.TemplateResponse("index.html", context)
