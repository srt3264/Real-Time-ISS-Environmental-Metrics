# scripts/fetch_imf_bz.py

import requests
import sqlite3
import os
from datetime import datetime

DB_PATH = "data/iss_environment.db"

def fetch_imf_bz():
    url = "https://services.swpc.noaa.gov/products/solar-wind/mag-1-day.json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        rows = response.json()
    except Exception as e:
        print(f"Failed to fetch IMF Bz data: {e}")
        return

    if len(rows) < 2:
        print("No IMF Bz data available.")
        return

    headers = rows[0]
    data_rows = rows[1:]

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS imf_bz (
            time_tag TEXT,
            bx_gsm REAL,
            by_gsm REAL,
            bz_gsm REAL,
            bt REAL
        )
    """)

    inserted = 0
    for row in data_rows:
        try:
            time_tag = row[0]
            bx = float(row[1]) if row[1] else None
            by = float(row[2]) if row[2] else None
            bz = float(row[3]) if row[3] else None
            bt = float(row[6]) if row[6] else None  # Bt total field

            conn.execute("""
                INSERT INTO imf_bz (time_tag, bx_gsm, by_gsm, bz_gsm, bt)
                VALUES (?, ?, ?, ?, ?)
            """, (time_tag, bx, by, bz, bt))

            inserted += 1
        except Exception as e:
            print(f"Skipped row due to error: {e}")

    conn.commit()
    conn.close()
    print(f"Fetched and stored {inserted} IMF Bz records.")

if __name__ == "__main__":
    fetch_imf_bz()