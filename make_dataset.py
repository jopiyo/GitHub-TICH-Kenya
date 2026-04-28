import pandas as pd
from sklearn.impute import SimpleImputer

def clean_climate_data(input_path, output_path):
    # Load raw weather station data
    df = pd.read_csv(input_path)
    
    # Handle missing values using mean imputation for Siaya's climate
    imputer = SimpleImputer(strategy='mean')
    df[['avg_temp', 'rainfall_mm']] = imputer.fit_transform(df[['avg_temp', 'rainfall_mm']])
    
    # Save to processed folder
    df.to_csv(output_path, index=False)
    print(f"Data cleaned and saved to {output_path}")

if __name__ == "__main__":
    clean_climate_data('../../data/raw/climate_stations_hourly.csv', 
                       '../../data/processed/historical_trends.csv')
