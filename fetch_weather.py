import requests
import pandas as pd
from datetime import date, timedelta

cities = {
    "Delhi": (28.61, 77.21), "Mumbai": (19.08, 72.88),
    "Chennai": (13.08, 80.27), "Bengaluru": (12.97, 77.59),
    "Kolkata": (22.57, 88.36), "Hyderabad": (17.39, 78.49),
    "Ahmedabad": (23.02, 72.57), "Pune": (18.52, 73.86),
    "Lucknow": (26.85, 80.95), "Tirunelveli": (8.73, 77.70),
}

today = date.today()
start = today - timedelta(days=90)
archive_end = today - timedelta(days=6)
hourly = "temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation"

frames = []
for city, (lat, lon) in cities.items():
    old = requests.get("https://archive-api.open-meteo.com/v1/archive", params={
        "latitude": lat, "longitude": lon,
        "start_date": start.isoformat(), "end_date": archive_end.isoformat(),
        "hourly": hourly, "timezone": "Asia/Kolkata"}).json()
    new = requests.get("https://api.open-meteo.com/v1/forecast", params={
        "latitude": lat, "longitude": lon, "hourly": hourly,
        "past_days": 10, "forecast_days": 1, "timezone": "Asia/Kolkata"}).json()
    if "hourly" not in old or "hourly" not in new:
        print(city, old.get("reason"), new.get("reason"))
        raise SystemExit("API error, try again in a minute")
    both = pd.concat([pd.DataFrame(old["hourly"]), pd.DataFrame(new["hourly"])])
    both = both.groupby("time", as_index=False).first()
    both["city"] = city
    frames.append(both)
    print(f"Done: {city} ({len(both)} rows)")

final = pd.concat(frames, ignore_index=True)
final.to_csv("data/raw/weather_all.csv", index=False)
print(final.shape)