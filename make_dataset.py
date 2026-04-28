import pandas as pd
import numpy as np
import os
from sklearn.impute import SimpleImputer

# Define directory paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'climate_stations_hourly.csv')
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'historical_trends.csv')

def preprocess_climate_data(input_path, output_path):
    """
    Cleans raw sensor data and prepares it for the ClimateGuard model.
    """
    if not os.path.exists(input_path):
        print(f"Error: Raw data file not found at {input_path}")
        return

    print(f"Reading raw data from: {input_path}")
    df = pd.read_csv(input_path)

    # 1. Handle Missing Values
    # In the Lake Victoria Basin, sudden sensor dropouts are common due to power fluctuations.
    # We use 'mean' for temperature/humidity and '0' for rainfall to avoid false alerts.
    imputer_mean = SimpleImputer(strategy='mean')
    df[['temp_c', 'humidity_pct']] = imputer_mean.fit_transform(df[['temp_c', 'humidity_pct']])
    
    df['rainfall_mm'] = df['rainfall_mm'].fillna(0)

    # 2. Feature Engineering: Moving Averages
    # Outbreaks aren't triggered by a single hour of rain, but by sustained wetness.
    # We calculate a 24-hour rolling average for rainfall and stagnant water.
    df['rolling_rain_24h'] = df.groupby('station_id')['rainfall_mm'].transform(
        lambda x: x.rolling(window=24, min_periods=1).mean()
    )

    # 3. Validation & Type Casting
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Ensure the columns match the expected input order for inference.py
    # ['rainfall_mm', 'temp_c', 'humidity_pct', 'stagnant_water_index']
    final_cols = ['timestamp', 'station_id', 'rainfall_mm', 'temp_c', 
                  'humidity_pct', 'stagnant_water_index', 'rolling_rain_24h']
    
    df_processed = df[final_cols]

    # 4. Save Processed Data
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_processed.to_csv(output_path, index=False)
    print(f"Successfully saved processed data to: {output_path}")

if __name__ == "__main__":
    preprocess_climate_data(RAW_DATA_PATH, PROCESSED_DATA_PATH)
