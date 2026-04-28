import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

def train_climateguard():
    # Load historical TICH data (Climate vs. Case counts)
    df = pd.read_csv('../data/processed/historical_trends.csv')
    
    # Features: Rainfall, Temp, Humidity, Stagnant Water Index
    X = df[['rainfall_mm', 'avg_temp', 'humidity', 'stagnant_water_idx']]
    # Target: Outbreak_Occurred (Binary)
    y = df['outbreak_occurred']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Using Random Forest for interpretability in public health
    model = RandomForestClassifier(n_estimators=100, max_depth=10)
    model.fit(X_train, y_train)
    
    # Save the model for production use
    joblib.dump(model, 'climateguard_v1_model.pkl')
    print("Model training complete. Serialized as climateguard_v1_model.pkl")

if __name__ == "__main__":
    train_climateguard()
