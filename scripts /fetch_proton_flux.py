# scripts/fetch_proton_flux.py

import requests
import sqlite3

DB_PATH = "data/iss_environment.db"
URL = "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-1-day.json"

def fetch_proton_flux():
    response = requests.get(URL)
    data = response.json()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goes_proton_flux (
            time_tag TEXT,
            satellite INTEGER,
            energy TEXT,
            energy_units TEXT,
            flux REAL,
            flux_units TEXT,
            PRIMARY KEY (time_tag, satellite, energy)
        )
    """)

    for entry in data:
        cursor.execute("""
            INSERT OR REPLACE INTO goes_proton_flux (time_tag, satellite, energy, energy_units, flux, flux_units)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            entry.get("time_tag"),
            entry.get("satellite"),
            entry.get("energy"),
            entry.get("energy_units", "MeV"),  # fallback default
            entry.get("flux"),
            entry.get("flux_units", "pfu")     # fallback default
        ))

    conn.commit()
    conn.close()
    print(f"Fetched {len(data)} proton flux records.")

if __name__ == "__main__":
    fetch_proton_flux()