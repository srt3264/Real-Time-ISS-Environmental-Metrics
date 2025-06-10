import streamlit as st
import sqlite3
import pandas as pd
import time

st.query_params.update({"page": "home"})

st.title("🚀 Real-Time ISS Environmental Dashboard")
st.write("Most recent telemetry updates (auto-refresh every 10 seconds):")

conn = sqlite3.connect("../data/iss_environment.db")
df = pd.read_sql_query("SELECT * FROM iss_telemetry ORDER BY timestamp DESC LIMIT 100", conn)
conn.close()

df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
df = df.sort_values('datetime')

st.dataframe(df)

latest_item = df['item'].iloc[0]
chart_df = df[df['item'] == latest_item].copy()
chart_df = chart_df.sort_values('datetime')

st.subheader(f"📈 Value trend for '{latest_item}'")
st.line_chart(chart_df.set_index('datetime')['value'])

if st.button("🔄 Refresh Now"):
    st.rerun()

interval = st.selectbox("Refresh interval (seconds):", [1, 5, 10], index=0)
time.sleep(interval)
st.rerun()