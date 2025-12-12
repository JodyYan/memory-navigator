import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_telemetry():
    url = f"{BASE_URL}/api/v1/ingestion/telemetry"
    payload = {
        "device_id": "test_device",
        "records": [
            {
                "timestamp": "2023-10-27T10:00:00Z",
                "location": { "lat": 37.77, "lon": -122.41, "accuracy": 10.0 },
                "vitals": { "heart_rate": 70, "steps": 100 },
                "battery_level": 90
            }
        ]
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"Telemetry Test: PASS ({response.json()})")
    except Exception as e:
        print(f"Telemetry Test: FAIL ({e})")
        sys.exit(1)

def test_event():
    url = f"{BASE_URL}/api/v1/ingestion/events"
    payload = {
        "device_id": "test_device",
        "timestamp": "2023-10-27T10:05:00Z",
        "event_type": "FALL_DETECTED",
        "details": { "lat": 37.77, "lon": -122.41, "description": "Fall detected" }
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"Event Test: PASS ({response.json()})")
    except Exception as e:
        print(f"Event Test: FAIL ({e})")
        sys.exit(1)

if __name__ == "__main__":
    print("Starting API Tests...")
    test_telemetry()
    test_event()
    print("All API Tests Passed.")
