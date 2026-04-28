import pandas as pd
from joblib import load

# Load the pre-trained ClimateGuard model
model = load('../models/health_predictor_v1.pkl')

def predict_outbreak_risk(input_csv):
    data = pd.read_csv(input_csv)
    # Features: [Avg_Temp, Rainfall_mm, Humidity]
    predictions = model.predict(data[['temp', 'rain', 'humidity']])
    
    data['outbreak_risk'] = predictions
    data.to_csv('../data/current_projections.csv', index=False)
    print("Outbreak risk analysis complete. Results saved to /data.")

if __name__ == "__main__":
    predict_outbreak_risk('../data/recent_weather_summary.csv')
