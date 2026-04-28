-- Initial Schema for ClimateGuard
CREATE TABLE climate_records (
    id SERIAL PRIMARY KEY,
    location_name VARCHAR(100),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    temperature DECIMAL,
    rainfall_mm DECIMAL,
    humidity INT
);

CREATE TABLE health_alerts (
    id SERIAL PRIMARY KEY,
    sub_county VARCHAR(100),
    risk_level VARCHAR(20), -- GREEN, YELLOW, RED
    triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
