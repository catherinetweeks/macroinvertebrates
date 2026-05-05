
import requests
from datetime import datetime, timedelta

def get_noaa_data(target_date_string):
    # Convert input date
    target_date = datetime.strptime(target_date_string, "%Y-%m-%d")
    start_date = target_date - timedelta(days=30)



    API_KEY = "kYHBqHiWargKOBvXJZzYAUJKbeBiimlx"
    
    url = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"
    
    headers = {
        "token": API_KEY
    }
    
    params = {
        "datasetid": "GHCND",
        "stationid": "GHCND:USC00190120",
        "units": "standard",
        "startdate": start_date.strftime("%Y-%m-%d"),
        "enddate": target_date.strftime("%Y-%m-%d"),
        "datatypeid": ["PRCP", "Tmin", "Tmax"]
    }

    print(start_date)
    print(target_date)
    
    response = requests.get(url, headers=headers, params=params)


    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return None

    data = response.json().get("results", [])

    if not data:
        print("No data returned")
        return None

    # Extract values
    values = [entry["value"] for entry in data if "value" in entry]

    if not values:
        print("No valid values found")
        return None

    avg = sum(values) / len(values)
    print(avg)
    return avg

# get_noaa_data("2025-05-05")