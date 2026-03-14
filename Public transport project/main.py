import requests
import pandas as pd
import configuration
from tabulate import tabulate
# -----------------------------
# Function to fetch Train Alerts
# -----------------------------
def fetch_alerts():
    try:
        response = requests.get(configuration.ALERTS_URL, headers=configuration.HEADERS)
        alerts = response.json()
        rows = []

        # Check service status
        status = alerts["value"].get("Status", 1)

        if status == 2:
            # Disrupted service
            segments = alerts["value"].get("AffectedSegments", [])
            if segments:
                # Loop through each affected segment
                for seg in segments:
                    rows.append({
                        "Affected Train Line": seg.get("Line", "Unknown"),
                        "Direction of Breakdown": seg.get("Direction", "Unknown"),
                        "Affected Stations": seg.get("Stations", "Unknown"),
                        "Alternate Travel Options": seg.get("FreePublicBus", "None"),
                        "Shuttle Services": seg.get("FreeMRTShuttle", "None")
                    })
            else:
                # Status=2 but no segment details
                rows.append({
                    "Affected Train Line": "Unknown",
                    "Direction of Breakdown": "Unknown",
                    "Affected Stations": "Unknown",
                    "Alternate Travel Options": "Unknown",
                    "Shuttle Services": "Unknown"
                })
        else:
            # Normal service
            rows.append({
                "Affected Train Line": "-",
                "Direction of Breakdown": "-",
                "Affected Stations": "-",
                "Alternate Travel Options": "-",
                "Shuttle Services": "-"
            })

            # Create DataFrame
            df = pd.DataFrame(rows)

            # Display as pretty table
            print(tabulate(df, headers="keys", tablefmt="grid"))
        
    except:
        return ["Could not fetch alerts"]

# -----------------------------
# Main Analysis
# -----------------------------
def analyze_mrt():
    df = fetch_alerts()
    print("Train Service Alerts DataFrame:", df)

    
# Run the analyzer
if __name__ == "__main__":
    analyze_mrt()