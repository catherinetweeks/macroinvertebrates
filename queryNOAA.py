
import requests
from datetime import datetime, timedelta

API_KEY = "kYHBqHiWargKOBvXJZzYAUJKbeBiimlx"
    
url = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"
    
headers = {
    "token": API_KEY
}

def get_mon_prcp(target_date_string):
    # Convert input date
    target_date = datetime.strptime(target_date_string, "%Y-%m-%d")
    start_date = target_date - timedelta(days=30)
    
    params = {
        "datasetid": "GHCND",
        "stationid": "GHCND:USC00190120",
        "units": "standard",
        "startdate": start_date.strftime("%Y-%m-%d"),
        "enddate": target_date.strftime("%Y-%m-%d"),
        "datatypeid": ["PRCP"]
    }
    
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
    return avg

def get_mon_add(target_date_string):
    # Convert input date
    target_date = datetime.strptime(target_date_string, "%Y-%m-%d")
    start_date = target_date - timedelta(days=30)
    
    params = {
        "datasetid": "GHCND",
        "stationid": "GHCND:USC00190120",
        "units": "standard",
        "startdate": start_date.strftime("%Y-%m-%d"),
        "enddate": target_date.strftime("%Y-%m-%d"),
        "datatypeid": ["Tmin", "Tmax"]
    }
    
    response = requests.get(url, headers=headers, params=params)


    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return None

    data = response.json().get("results", [])

# Group temps by date
    temps_by_date = {}

    for entry in data:

        date = entry["date"][:10]
        datatype = entry["datatype"]
        value = entry["value"]

        if date not in temps_by_date:
            temps_by_date[date] = {}

        temps_by_date[date][datatype] = value

    daily_averages = []

    for date, values in temps_by_date.items():

        if "TMIN" in values and "TMAX" in values:

            tmin = values["TMIN"]
            tmax = values["TMAX"]

            daily_avg = (tmin + tmax) / 2

            daily_averages.append(daily_avg)

    if not daily_averages:
        print("No temperature data found")
        return None

    avg_temp_30_days = sum(daily_averages) / len(daily_averages)

    return avg_temp_30_days
