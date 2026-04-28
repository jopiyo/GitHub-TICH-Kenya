from fastapi import FastAPI
from src.api import alerts, climate

app = FastAPI(title="ClimateGuard API")

app.include_router(alerts.router, prefix="/v1/alerts")
app.include_router(climate.router, prefix="/v1/climate")

@app.get("/")
def health_check():
    return {"status": "operational", "version": "1.0.0"}
