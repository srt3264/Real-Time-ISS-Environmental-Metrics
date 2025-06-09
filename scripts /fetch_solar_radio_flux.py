# scripts/fetch_solar_radio_flux.py

import requests
import sqlite3

DB_PATH = "data/iss_environment.db"
URL = "https://services.swpc.noaa.gov/json/solar-cycle/predicted-solar-cycle.json"

def fetch_solar_radio_flux():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching solar radio flux data: {e}")
        return

    if not data:
        print("No solar radio flux data found.")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS solar_radio_flux (
            time_tag TEXT PRIMARY KEY,
            predicted_f10_7 REAL,
            predicted_ssn REAL,
            high_ssn REAL,
            low_ssn REAL
        )
    """)

    inserted = 0
    for entry in data:
        try:
            conn.execute("""
                INSERT OR REPLACE INTO solar_radio_flux 
                (time_tag, predicted_f10_7, predicted_ssn, high_ssn, low_ssn)
                VALUES (?, ?, ?, ?, ?)
            """, (
                entry["time-tag"],
                entry["predicted_f10.7"],
                entry["predicted_ssn"],
                entry["high_ssn"],
                entry["low_ssn"]
            ))
            inserted += 1
        except Exception as e:
            print(f"Skipped entry due to error: {e}")

    conn.commit()
    conn.close()
    print(f"✅ Stored {inserted} solar radio flux entries.")

if __name__ == "__main__":
    fetch_solar_radio_flux()