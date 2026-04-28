import requests
import os

# Configuration
API_KEY = os.getenv("WEATHER_API_KEY")
LOCATIONS = ["Kisumu", "Siaya", "Homa Bay"]

def get_climate_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},KE&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"Captured {city}: {data['main']['temp']}C, {data['weather'][0]['description']}")
        # Logic to save to PostgreSQL database goes here
    else:
        print(f"Failed to fetch data for {city}")

if __name__ == "__main__":
    for loc in LOCATIONS:
        get_climate_data(loc)
