import schedule
import time
import subprocess
from fetch_iss_location import fetch_iss_location
from fetch_astronauts import fetch_astronauts
from fetch_kp_index import fetch_kp_index
from fetch_goes_xray import fetch_goes_xray
from fetch_proton_flux import fetch_proton_flux
from fetch_electron_flux import fetch_electron_flux
from fetch_solar_wind import fetch_solar_wind
from fetch_xray_flux import fetch_xray_flux
from fetch_imf_bz import fetch_imf_bz
from fetch_solar_radio_flux import fetch_solar_radio_flux


print("Launching ISS telemetry stream...")
telemetry_proc = subprocess.Popen(["python", "/workspaces/Real-Time-ISS-Environmental-Metrics/scripts /stream_iss_telemetry.py"])


schedule.every(15).seconds.do(fetch_iss_location)
schedule.every().sunday.at("00:00").do(fetch_astronauts)
schedule.every(6).hours.do(fetch_kp_index) #API returns 1-minutealso, resolution geomagnetic Kp index data for approximately the last 6 hours.
schedule.every(3).hours.do(fetch_goes_xray)
schedule.every(6).hours.do(fetch_proton_flux)
schedule.every(15).minutes.do(fetch_electron_flux)
schedule.every(1).hours.do(fetch_solar_wind)
schedule.every(6).hours.do(fetch_xray_flux)
schedule.every(1).hours.do(fetch_imf_bz)    
schedule.every().day.at("01:00").do(fetch_solar_radio_flux)

print("Starting ISS tracking loop...")

while True:
    schedule.run_pending()
    time.sleep(1) 