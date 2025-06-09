# scripts/fetch_kp_index.py

import requests
import sqlite3
from datetime import datetime

DB_PATH = "data/iss_environment.db"
URL = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"

def fetch_kp_index():
    response = requests.get(URL)
    data = response.json()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS solar_kp_index (
            time_tag TEXT PRIMARY KEY,
            kp_index REAL
        )
    """)

    for entry in data:
        time_tag = entry["time_tag"]
        kp = entry["kp_index"]
        cursor.execute("""
            INSERT OR REPLACE INTO solar_kp_index (time_tag, kp_index)
            VALUES (?, ?)
        """, (time_tag, kp))

    conn.commit()
    conn.close()
    print(f"Fetched {len(data)} Kp index records.")

if __name__ == "__main__":
    fetch_kp_index()