from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from models.inference import ClimateGuardInference
import uvicorn

# Initialize the API
app = FastAPI(
    title="ClimateGuard API",
    description="Intelligence backend for TICH climate-health monitoring",
    version="1.0.0"
)

# Enable CORS for the React Dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with your dashboard domain
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the inference engine
predictor = ClimateGuardInference()

# Define the data structure for incoming weather readings
class WeatherReading(BaseModel):
    station_id: str
    rainfall_mm: float
    temp_c: float
    humidity_pct: float
    stagnant_water_index: float

@app.get("/")
async def root():
    return {
        "status": "active",
        "region": "Lake Victoria Basin / Mageta Island",
        "model_version": "v1.0.4"
    }

@app.post("/v1/predict")
async def get_prediction(reading: WeatherReading):
    """
    Ingests live station data and returns an immediate health risk assessment.
    """
    # Prepare data for the model
    features = [
        reading.rainfall_mm, 
        reading.temp_c, 
        reading.humidity_pct, 
        reading.stagnant_water_index
    ]
    
    # Run Inference
    result = predictor.predict_risk(features)
    
    if not result:
        raise HTTPException(status_code=500, detail="Inference engine failure")
        
    return {
        "station": reading.station_id,
        "assessment": result
    }

@app.get("/v1/health-check")
async def health():
    # Basic uptime check for the HP ProLiant edge server
    return {"status": "operational", "engine": "loaded" if predictor.model else "error"}

if __name__ == "__main__":
    # Run server (standard for local dev or edge deployment)
    uvicorn.run(app, host="0.0.0.0", port=8000)
