# backend/db_manager.py

import sqlite3
import pandas as pd
from datetime import datetime, timedelta, timezone
import os 
DB_PATH = os.path.abspath(os.path.join(os.getcwd(), "data", "iss_environment.db"))

TABLE_TIME_INFO = {
    "iss_location": ("timestamp", "int"),
    "astronauts": ("timestamp", "str_datetime"),
    "iss_telemetry": ("timestamp", "float"),
    "solar_kp_index": ("time_tag", "iso8601"),
    "xray_flux": ("time_tag", "iso8601_z"),
    "proton_flux": ("time_tag", "iso8601_z"),
    "solar_wind": ("time_tag", "iso8601_z"),
    "goes_electron_flux": ("time_tag", "iso8601_z"),
    "solar_radio_flux": ("time_tag", "prefix"), 
}

def get_historical_data(table_name, start_dt=None, end_dt=None, limit=None):
    time_col, time_type = TABLE_TIME_INFO[table_name]

    if start_dt is None:
        start_dt = datetime.now(timezone.utc) - timedelta(hours=1)
    if end_dt is None:
        end_dt = datetime.now(timezone.utc)

    if time_type == "int":
        start = int(start_dt.timestamp())
        end = int(end_dt.timestamp())
    elif time_type == "float":
        start = start_dt.timestamp() / 1000
        end = end_dt.timestamp() / 1000
    elif time_type == "str_datetime":
        start = start_dt.strftime("%-m/%-d/%Y %H:%M")
        end = end_dt.strftime("%-m/%-d/%Y %H:%M")
    elif time_type == "iso8601":
        start = start_dt.strftime("%Y-%m-%dT%H:%M:%S")
        end = end_dt.strftime("%Y-%m-%dT%H:%M:%S")
    elif time_type == "iso8601_z":
        start = start_dt.strftime("%Y-%m-%d %H:%M:%S")
        end = end_dt.strftime("%Y-%m-%d %H:%M:%S")
    elif time_type == "prefix":
        start = start_dt.strftime("%Y-%m")
        end = end_dt.strftime("%Y-%m")
    else:
        raise ValueError("Unknown time type")
    print(start, end)


    query = f"""
        SELECT * FROM {table_name}
        WHERE {time_col} >= ? AND {time_col} <= ?
    """
    params = [start, end]

    if limit:
        query += " LIMIT ?"
        params.append(limit)

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(query, conn, params=params)
    conn.close()

    return df

def get_latest_timestamp(table_name):
    time_col, _ = TABLE_TIME_INFO[table_name]
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT MAX({time_col}) FROM {table_name}")
    result = cursor.fetchone()[0]
    conn.close()
    return result


