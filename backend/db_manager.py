# backend/db_manager.py

import sqlite3
import pandas as pd
from datetime import datetime, timedelta, timezone

DB_PATH = "../data/iss_environment.db"

def get_historical_data(timestamp_col, table_name, start_time_str=None, end_time_str=None, limit=None): 
    conn = sqlite3.connect(DB_PATH)

    query = (f"""
            select * 
            from {table_name}
            where {timestamp_col} >= {start_time_str}
            and {timestamp_col} <= {end_time_str}
            limit 5
        """)

    
    df = pd.read_sql(query, conn)

    return df