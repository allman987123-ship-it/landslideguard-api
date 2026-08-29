from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime, timezone

app = FastAPI(
    title="LandslideGuard AI",
    description="SIH26001 Landslide Early Warning System",
    version="1.0.0"
)


class SensorData(BaseModel):
    rainfall: float
    soil_moisture: float
    temperature: float
    humidity: float
    latitude: float
    longitude: float


latest_data = {
    "rainfall": 76,
    "soil_moisture": 91,
    "temperature": 27,
    "humidity": 84,
    "latitude": 25.467,
    "longitude": 91.366,
    "risk_score": 72,
    "risk_level": "HIGH",
    "updated_at": None
}


def calculate_risk(data: SensorData):

    score = 0

    if data.rainfall >= 80:
        score += 40
    elif data.rainfall >= 50:
        score += 25
    elif data.rainfall >= 20:
        score += 10

    if data.soil_moisture >= 90:
        score += 35
    elif data.soil_moisture >= 75:
        score += 25
    elif data.soil_moisture >= 60:
        score += 10

    score = min(score, 100)

    if score >= 80:
        level = "CRITICAL"
    elif score >= 60:
        level = "HIGH"
    elif score >= 30:
        level = "MODERATE"
    else:
        level = "LOW"

    return score, level


# ==========================
# DASHBOARD
# ==========================

@app.get("/")
def dashboard():
    return FileResponse("dashboard/index.html")


# ==========================
# HEALTH CHECK
# ==========================

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "LandslideGuard AI"
    }


# ==========================
# SENSOR API
# ==========================

@app.post("/api/sensor")
def receive_sensor_data(data: SensorData):

    risk_score, risk_level = calculate_risk(data)

    latest_data.update({
        "rainfall": data.rainfall,
        "soil_moisture": data.soil_moisture,
        "temperature": data.temperature,
        "humidity": data.humidity,
        "latitude": data.latitude,
        "longitude": data.longitude,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "updated_at": datetime.now(timezone.utc).isoformat()
    })

    return {
        "success": True,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "data": latest_data
    }


# ==========================
# LATEST DATA
# ==========================

@app.get("/api/latest")
def get_latest_data():

    return latest_data