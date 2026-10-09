import requests
import pandas as pd

url = "https://air-quality-api.open-meteo.com/v1/air-quality"
params = {
    "latitude": 13.08,
    "longitude": 80.27,
    "hourly": "pm2_5,pm10,us_aqi",
    "past_days": 7,
    "forecast_days": 1,
    "timezone": "Asia/Kolkata",
}

data = requests.get(url, params=params).json()
df = pd.DataFrame(data["hourly"])
df["city"] = "Chennai"

df.to_csv("data/raw/chennai.csv", index=False)
print(df.head())
print(df.shape)