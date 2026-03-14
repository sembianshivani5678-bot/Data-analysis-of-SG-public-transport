import requests
import pandas as pd

# -----------------------------
# LTA API details
# -----------------------------
API_KEY = "Vr9HWuiUS0K+SAPW2LtWeA=="
ALERTS_URL = "https://datamall2.mytransport.sg/ltaodataservice/TrainServiceAlerts"

HEADERS = {
    "AccountKey": API_KEY,
    "accept": "application/json"
}
# -----------------------------
# Function to fetch Train Alerts
# -----------------------------
def fetch_alerts():
    try:
        response = requests.get(ALERTS_URL, headers=HEADERS)
        alerts = response.json()
        rows = []
        print("Processing Train Service Alerts...", alerts.get("value", []))
        if alerts["value"]["Status"] == 2:
            segments = alerts["value"]["AffectedSegments"]
            for seg in segments:
                rows.append({
                "Affected Train Line": seg.get("Line"),
                "Direction of Breakdown": seg.get("Direction"),
                "Affected Stations": seg.get("Stations"),
                "Alternate Travel Options": seg.get("FreePublicBus"),
                "Shuttle Services": seg.get("FreeMRTShuttle")
            })
            print("Fetched Train Service Alerts successfully.", len(rows), "alerts found.")
        else:
            print("No train service breakdowns currently.")
    
    except:
        return ["Could not fetch alerts"]
    
# Run the analyzer
if __name__ == "__main__":
    fetch_alerts()