import joblib
from sklearn.preprocessing import StandardScaler
import pandas as pd

def create_and_save_scaler():
    # Load your training data
    df = pd.read_csv('../data/processed/historical_trends.csv')
    features = df[['rainfall_mm', 'avg_temp', 'humidity', 'stagnant_water_idx']]
    
    # Initialize and fit the scaler
    scaler = StandardScaler()
    scaler.fit(features)
    
    # Save it to the models folder
    joblib.dump(scaler, 'feature_scaler.pkl')
    print("feature_scaler.pkl has been created successfully.")

if __name__ == "__main__":
    create_and_save_scaler()
