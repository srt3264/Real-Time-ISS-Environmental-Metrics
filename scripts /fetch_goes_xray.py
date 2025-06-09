# scripts/fetch_goes_xray.py

import requests
import sqlite3

DB_PATH = "data/iss_environment.db"
URL = "https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json"

def fetch_goes_xray():
    response = requests.get(URL)
    data = response.json()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goes_xray_flux (
            time_tag TEXT,
            satellite INTEGER,
            energy TEXT,
            flux REAL,
            PRIMARY KEY (time_tag, satellite, energy)
        )
    """)

    for entry in data:
        cursor.execute("""
            INSERT OR REPLACE INTO goes_xray_flux (time_tag, satellite, energy, flux)
            VALUES (?, ?, ?, ?)
        """, (
            entry["time_tag"],
            entry["satellite"],
            entry["energy"],
            entry["flux"]
        ))

    conn.commit()
    conn.close()
    print(f"Fetched {len(data)} X-ray flux records.")

if __name__ == "__main__":
    fetch_goes_xray()