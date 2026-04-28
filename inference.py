import joblib
import pandas as pd
import numpy as np
import os
from datetime import datetime

# Path configuration
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'climateguard_v1_model.pkl')
SCALER_PATH = os.path.join(os.path.dirname(__file__), 'feature_scaler.pkl')

class ClimateGuardInference:
    def __init__(self):
        """Initialize by loading the trained model and standardized scaler."""
        try:
            self.model = joblib.load(MODEL_PATH)
            self.scaler = joblib.load(SCALER_PATH)
            print("ClimateGuard: Model and Scaler loaded successfully.")
        except FileNotFoundError as e:
            print(f"Error: Missing model files. Ensure training is complete. {e}")
            self.model = None

    def predict_risk(self, climate_features):
        """
        Takes raw climate features and returns a binary prediction and probability.
        Input format: [rainfall_mm, avg_temp, humidity, stagnant_water_idx]
        """
        if self.model is None:
            return None

        # Convert input to numpy array and reshape for single prediction
        features_array = np.array(climate_features).reshape(1, -1)
        
        # 1. Apply the exact same scaling used during training
        scaled_features = self.scaler.transform(features_array)
        
        # 2. Generate Prediction (0 = Stable, 1 = High Risk)
        prediction = self.model.predict(scaled_features)[0]
        
        # 3. Generate Confidence Score (Probability of Outbreak)
        probability = self.model.predict_proba(scaled_features)[0][1]
        
        return {
            "risk_level": "HIGH" if prediction == 1 else "STABLE",
            "outbreak_probability": round(float(probability), 4),
            "timestamp": datetime.now().isoformat()
        }

    def batch_process(self, input_csv, output_csv):
        """Processes a raw CSV and appends predictions."""
        df = pd.read_csv(input_csv)
        
        # Ensure we only pass the 4 features the model expects
        feature_cols = ['rainfall_mm', 'temp_c', 'humidity_pct', 'stagnant_water_index']
        
        # Scale and predict
        scaled_data = self.scaler.transform(df[feature_cols])
        df['risk_probability'] = self.model.predict_proba(scaled_data)[:, 1]
        df['risk_label'] = np.where(df['risk_probability'] > 0.5, 'HIGH', 'STABLE')
        
        df.to_csv(output_csv, index=False)
        print(f"Batch inference complete. Results saved to {output_csv}")

if __name__ == "__main__":
    # Example Usage
    inference = ClimateGuardInference()
    
    # Mock data point: [Rainfall 12.5mm, Temp 22.8C, Humidity 95%, Water Index 0.68]
    test_data = [12.5, 22.8, 95, 0.68]
    result = inference.predict_risk(test_data)
    
    print(f"Prediction Result: {result}")
