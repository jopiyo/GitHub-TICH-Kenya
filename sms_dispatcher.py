import requests
import africastalking
import os

# Initialize Africa's Talking (Standard for Kenya/Siaya region)
# In production, these should be environment variables
USERNAME = "sandbox" # or your AT username
API_KEY = "your_api_key_here"
africastalking.initialize(USERNAME, API_KEY)
sms = africastalking.SMS

# Configuration
API_ENDPOINT = "http://localhost:8000/v1/predict"
# List of CHPs (Community Health Promoters) for Mageta Island
RECIPIENTS = ["+254700000000", "+254711111111"] 

def check_and_alert():
    # 1. Fetch current climate data (Mocking a station reading)
    # In a real loop, this would pull from your data/raw/ file
    current_reading = {
        "station_id": "MAG-001",
        "rainfall_mm": 15.5,
        "temp_c": 24.5,
        "humidity_pct": 92.0,
        "stagnant_water_index": 0.75
    }

    try:
        # 2. Get prediction from your FastAPI backend
        response = requests.post(API_ENDPOINT, json=current_reading)
        data = response.json()
        
        assessment = data.get("assessment", {})
        risk_level = assessment.get("risk_level")
        probability = assessment.get("outbreak_probability")

        # 3. Disseminate if Risk is HIGH
        if risk_level == "HIGH":
            message = (
                f"CLIMATEGUARD ALERT: High health risk detected at Station {data['station']}. "
                f"Probability: {probability*100}%. Please check your Moodle LMS for "
                f"prevention protocols. - TICH EWS"
            )
            
            # Send SMS
            response = sms.send(message, RECIPIENTS)
            print(f"Alert Sent: {response}")
        else:
            print(f"Condition Stable. Probability: {probability}")

    except Exception as e:
        print(f"Dispatcher Error: {e}")

if __name__ == "__main__":
    check_and_alert()
