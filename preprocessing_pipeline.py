from sklearn.preprocessing import StandardScaler
import joblib

def save_scaler(data):
    scaler = StandardScaler()
    scaler.fit(data)
    joblib.dump(scaler, 'feature_scaler.pkl')
    return scaler

# Logic to handle missing climate values (Imputation)
def handle_missing_weather(df):
    return df.fillna(df.mean())
