# fetch_iss_location.py

import requests
import sqlite3
import pandas as pd
from datetime import datetime, timezone

def fetch_iss_location():
    # API call to Open Notify
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url)
    data = response.json()

    # pull and format data
    timestamp = data["timestamp"]
    dt_utc = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    latitude = float(data["iss_position"]["latitude"])
    longitude = float(data["iss_position"]["longitude"])

    df = pd.DataFrame([{
        "timestamp": timestamp,
        "datetime_utc": dt_utc,
        "latitude": latitude,
        "longitude": longitude
    }])

    # connect to sqlite and save
    conn = sqlite3.connect("data/iss_environment.db")
    df.to_sql("iss_location", conn, if_exists="append", index=False)
    conn.close()

    print("ISS location saved:", df.to_dict(orient="records")[0])

if __name__ == "__main__":
    fetch_iss_location()