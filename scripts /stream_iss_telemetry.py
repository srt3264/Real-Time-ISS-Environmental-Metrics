# scripts/stream_iss_telemetry.py

from lightstreamer.client import LightstreamerClient, Subscription, SubscriptionListener
import sqlite3
import os
import time

db_path = "data/iss_environment.db"
with sqlite3.connect(db_path) as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS iss_telemetry (
            timestamp REAL,
            item TEXT,
            value REAL,
            status_class TEXT,
            status_indicator TEXT
        )
    """)

items = [
    "USLAB000032",  # Cabin Temperature
    "USLAB000033",  # Cabin Pressure
    "USLAB000034",  # Cabin Humidity
    "NODE3000010",  # CO₂ Concentration
    "NODE3000012",  # O₂ Percentage
    "NODE3000005",  # Radiation Dosimeter
    "AIRLOCK000005",  # Pressure or other sensor in airlock
    "S0000005",       # Confirmed changing telemetry
    "RADDOSE_EXT",    # External Radiation Dose
]
fields = ["TimeStamp", "Value", "Status.Class", "Status.Indicator"]

client = LightstreamerClient("https://push.lightstreamer.com", "ISSLIVE")

print("Connecting to Lightstreamer...")
client.connect()
print("Connected, subscribing...")

sub = Subscription("MERGE", items, fields)

class TelemetryListener(SubscriptionListener):
    def onSubscription(self):
        print("Subscription to telemetry items successful.")

    def onSubscriptionError(self, code, message):
        print(f"Subscription error {code}: {message}")

    def onItemUpdate(self, update):
        print("Update received")
        for field in fields:
            print(f"{field}: {update.getValue(field)}")

        try:
            data = {
                "timestamp": update.getValue("TimeStamp"),
                "item": update.getItemName(),
                "value": update.getValue("Value"),
                "status_class": update.getValue("Status.Class"),
                "status_indicator": update.getValue("Status.Indicator")
            }
            print(f"{data['timestamp']} | {data['item']} = {data['value']}")

            conn = sqlite3.connect(db_path)
            conn.execute("""
                INSERT INTO iss_telemetry (timestamp, item, value, status_class, status_indicator)
                VALUES (?, ?, ?, ?, ?)
            """, (data["timestamp"], data["item"], data["value"], data["status_class"], data["status_indicator"]))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error parsing update or writing to DB: {e}")


sub.addListener(TelemetryListener())
client.subscribe(sub)

print("Listening for ISS telemetry updates...")
while True:
    time.sleep(1)