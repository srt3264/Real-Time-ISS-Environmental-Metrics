import requests
import sqlite3

DB_PATH = "data/iss_environment.db"
URL = "https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json"

def fetch_solar_wind():
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        raw_data = response.json()
    except Exception as e:
        print(f"Error fetching solar wind data: {e}")
        return

    if not raw_data or len(raw_data) < 2:
        print("No data returned from the solar wind API.")
        return

    headers = raw_data[0]
    records = raw_data[1:]

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS solar_wind (
            time_tag TEXT PRIMARY KEY,
            density REAL,
            speed REAL,
            temperature REAL
        )
    """)

    inserted = 0
    for row in records:
        try:
            record = dict(zip(headers, row))
            cursor.execute("""
                INSERT OR REPLACE INTO solar_wind (time_tag, density, speed, temperature)
                VALUES (?, ?, ?, ?)
            """, (
                record["time_tag"],
                float(record["density"]),
                float(record["speed"]),
                float(record["temperature"])
            ))
            inserted += 1
        except Exception as e:
            print(f"⚠️ Skipped row due to error: {e}")

    conn.commit()
    conn.close()
    print(f"Fetched and stored {inserted} solar wind records.")

if __name__ == "__main__":
    fetch_solar_wind()