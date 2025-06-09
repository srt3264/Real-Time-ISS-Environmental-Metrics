# scripts/fetch_xray_flux.py

import requests
import sqlite3
import os
from datetime import datetime

def fetch_xray_flux():
    url = "https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching X-ray flux data: {e}")
        return

    db_path = "data/iss_environment.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS xray_flux (
            time_tag TEXT,
            satellite TEXT,
            energy TEXT,
            flux REAL
        )
    """)

    inserted = 0
    for entry in data:
        try:
            cursor.execute("""
                INSERT INTO xray_flux (time_tag, satellite, energy, flux)
                VALUES (?, ?, ?, ?)
            """, (
                entry["time_tag"],
                entry["satellite"],
                entry["energy"],
                float(entry["flux"])
            ))
            inserted += 1
        except Exception as e:
            print(f"Skipped row due to error: {e}")

    conn.commit()
    conn.close()
    print(f"Fetched and stored {inserted} X-ray flux records.")

if __name__ == "__main__":
    fetch_xray_flux()