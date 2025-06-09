# scripts/fetch_astronauts.py

import requests
import sqlite3
import pandas as pd
from datetime import datetime, timezone
import os

os.makedirs("data", exist_ok=True)

def fetch_astronauts():
    url = "http://api.open-notify.org/astros.json"
    response = requests.get(url)
    data = response.json()
    
    current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    people = data["people"]

    df = pd.DataFrame(people)
    df["timestamp"] = current_time

    df = df[df["craft"] == "ISS"]

    conn = sqlite3.connect("data/iss_environment.db")
    df.to_sql("astronauts", conn, if_exists="append", index=False)
    conn.close()

    print(f"Saved {len(df)} ISS astronauts at {current_time}")

if __name__ == "__main__":
    fetch_astronauts()