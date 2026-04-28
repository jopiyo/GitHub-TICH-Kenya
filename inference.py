import joblib
import numpy as np

# 1. Load the model and the scaler
model = joblib.load('../models/climateguard_v1_model.pkl')
scaler = joblib.load('../models/feature_scaler.pkl')

def get_realtime_prediction(new_weather_data):
    # new_weather_data = [Rainfall, Temp, Humidity, Water_Index]
    # Example: [45.2, 28.5, 80, 0.5]
    
    # IMPORTANT: Scale the data using the saved scaler
    scaled_data = scaler.transform([new_weather_data])
    
    # Make the prediction
    prediction = model.predict(scaled_data)
    return "RED ALERT" if prediction[0] == 1 else "GREEN"

# Example Run
current_weather = [12.5, 30.2, 75, 0.2]
print(f"Current Health Risk Status: {get_realtime_prediction(current_weather)}")
