# 🌌 Real-Time ISS Environmental Metrics

This project collects real-time telemetry and space weather data to **forecast International Space Station (ISS) cabin conditions** — including temperature, radiation, humidity, and more — based on orbital location, sun exposure, and solar activity.

---

## Project Goal

To build a predictive model that estimates key **cabin environmental variables** on the ISS using:
- Onboard telemetry (e.g., radiation, temperature, humidity)
- ISS location and orbital parameters
- Solar weather indicators (e.g., solar wind, proton flux, X-ray flux)

The system streams and logs real-time data using scheduled API pulls and Lightstreamer subscriptions.

---

## Data Sources & API Descriptions

### 1. **ISS Telemetry** (via Lightstreamer)
Real-time sensor data from the ISS, streamed via [ISSLive!](https://isslive.com/).
- Data Adapter: `ISSLIVE`
- Sample Telemetry Items:
  - `USLAB000032` — Cabin Temperature
  - `USLAB000033` — Cabin Pressure
  - `USLAB000034` — Cabin Humidity
  - `NODE3000010` — CO₂ Concentration
  - `NODE3000012` — O₂ Percentage
  - `NODE3000005` — Radiation Dosimeter
  - `RADDOSE_EXT` — External Radiation Dose

### 2. **ISS Location** (Open Notify)
- API: [`http://api.open-notify.org/iss-now.json`](http://api.open-notify.org/iss-now.json)
- Returns latitude, longitude, and timestamp of the ISS.

### 3. **Current Astronauts** (Open Notify)
- API: [`http://api.open-notify.org/astros.json`](http://api.open-notify.org/astros.json)
- Returns list of astronauts and spacecraft.

### 4. **Solar Weather Data** (NOAA SWPC)
Collected from a range of NOAA services:
- **Kp Index**: Geomagnetic disturbance level (every 6 hrs)
- **GOES X-Ray Flux**: Solar flare intensity (every 3 hrs)
- **Proton Flux**: High-energy proton levels (every 6 hrs)
- **Electron Flux**: High-energy electron levels (every 15 min)
- **Solar Wind**: Density, speed, and temperature (every hour)
- **X-Ray Integrated Flux**: Summed solar X-ray energy (every 6 hrs)
- **IMF Bz**: North/South component of solar magnetic field (every hour)
- **Solar Radio Flux**: 10.7 cm flux for solar activity (daily)

---

## Project Structure
Real-Time-ISS-Environmental-Metrics/
│
├── data/                      # Logged sensor & solar data (SQLite)
│
├── scripts/                   # Data fetch scripts
│   ├── stream_iss_telemetry.py
│   ├── fetch_iss_location.py
│   ├── fetch_astronauts.py
│   ├── fetch_kp_index.py
│   ├── fetch_goes_xray.py
│   ├── fetch_proton_flux.py
│   ├── fetch_electron_flux.py
│   ├── fetch_solar_wind.py
│   ├── fetch_xray_flux.py
│   ├── fetch_imf_bz.py
│   └── fetch_solar_radio_flux.py
│
├── scheduler.py               # Master scheduling loop
├── requirements.txt           # Python package dependencies
└── README.md                  # Project overview (this file)

---

## Scheduling Frequency

Each API or stream is polled or run at an interval designed to balance freshness and system load:

| Source              | Interval         |
|---------------------|------------------|
| ISS Location        | Every 15 seconds |
| Astronauts          | Weekly (Sunday)  |
| Kp Index            | Every 6 hours    |
| GOES X-Ray          | Every 3 hours    |
| Proton Flux         | Every 6 hours    |
| Electron Flux       | Every 15 minutes |
| Solar Wind          | Every hour       |
| IMF Bz              | Every hour       |
| X-Ray Flux          | Every 6 hours    |
| Radio Flux          | Daily (1:00 AM)  |

---

## Variables Collected

### From ISS Telemetry:
| Variable              | Unit       | Description                          |
|-----------------------|------------|--------------------------------------|
| Temperature           | °C         | Internal cabin temp                  |
| Pressure              | kPa        | Cabin air pressure                   |
| Humidity              | %          | Cabin relative humidity              |
| Radiation             | μGy/hr     | Internal radiation dose              |
| External Radiation    | μGy/hr     | Outside station radiation dose       |
| CO₂ Concentration     | ppm        | Air carbon dioxide concentration     |
| O₂ Percentage         | %          | Oxygen fraction in atmosphere        |

### From Solar Weather:
| Variable              | Description                          |
|-----------------------|--------------------------------------|
| Kp Index              | Geomagnetic storm intensity (0–9)    |
| X-Ray Flux            | Solar flare strength (W/m²)          |
| Proton/Electron Flux  | Particle counts per cm²/s/sr/MeV     |
| Solar Wind Speed      | Plasma stream velocity (km/s)        |
| IMF Bz                | Interplanetary magnetic field (nT)   |
| Solar Radio Flux      | Proxy for solar activity (sfu)       |

---

## Next Steps

1. Let the system run for 14 days to log training data.
2. Begin exploratory data analysis (EDA).
3. Build predictive models (e.g., multivariate time series forecasting).
4. Optionally deploy a dashboard or API to monitor conditions in real time.

---

## Notes
- Ensure your EC2 instance has enough uptime to collect telemetry.
- Consider setting up data backups and logs to avoid loss.

---

## Contact

Maintained by [@srt3264](https://github.com/srt3264).  
Project started: **June 2025**  