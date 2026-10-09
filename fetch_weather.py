
import requests
import pandas as pd

cities = {
    "Delhi": (28.61, 77.21),
    "Mumbai": (19.08, 72.88),
    "Chennai": (13.08, 80.27),
    "Bengaluru": (12.97, 77.59),
    "Kolkata": (22.57, 88.36),
    "Hyderabad": (17.39, 78.49),
    "Ahmedabad": (23.02, 72.57),
    "Pune": (18.52, 73.86),
    "Lucknow": (26.85, 80.95),
    "Tirunelveli": (8.73, 77.70),
}

url = "https://api.open-meteo.com/v1/forecast"
all_data = []

for city, (lat, lon) in cities.items():
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation",
        "past_days": 7,
        "forecast_days": 1,
        "timezone": "Asia/Kolkata",
    }
    data = requests.get(url, params=params).json()
    df = pd.DataFrame(data["hourly"])
    df["city"] = city
    all_data.append(df)
    print(f"Done: {city} ({len(df)} rows)")

final = pd.concat(all_data, ignore_index=True)
final.to_csv("data/raw/weather_all.csv", index=False)
print(final.shape)