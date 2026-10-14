
import pandas as pd

aq = pd.read_csv("data/clean/air_quality_clean.csv", parse_dates=["time"])
w = pd.read_csv("data/raw/weather_all.csv", parse_dates=["time"])

w = w.rename(columns={
    "temperature_2m": "temperature",
    "relative_humidity_2m": "humidity",
    "wind_speed_10m": "wind_speed",
    "precipitation": "rain",
})

df = aq.merge(w, on=["city", "time"], how="inner")
df = df.dropna(subset=["temperature", "humidity", "wind_speed", "rain"])

df["rain_flag"] = (df["rain"] > 0).map({True: "Rainy", False: "Dry"})
df["wind_band"] = pd.cut(
    df["wind_speed"],
    bins=[-0.1, 5, 10, 1000],
    labels=["Calm (<5)", "Light (5-10)", "Windy (10+)"],
)
coords = {
    "Delhi": (28.61, 77.21), "Mumbai": (19.08, 72.88),
    "Chennai": (13.08, 80.27), "Bengaluru": (12.97, 77.59),
    "Kolkata": (22.57, 88.36), "Hyderabad": (17.39, 78.49),
    "Ahmedabad": (23.02, 72.57), "Pune": (18.52, 73.86),
    "Lucknow": (26.85, 80.95), "Tirunelveli": (8.73, 77.70),
}
df["latitude"] = df["city"].map(lambda c: coords[c][0])
df["longitude"] = df["city"].map(lambda c: coords[c][1])
df.to_csv("data/clean/air_quality_weather.csv", index=False)

print(df.shape)
print("Missing weather rows:", df["temperature"].isna().sum())
print(df.groupby("rain_flag")[["pm2_5", "us_aqi"]].mean().round(1))
print(df.groupby("wind_band", observed=True)[["pm2_5", "us_aqi"]].mean().round(1))
print(df[["pm2_5", "us_aqi", "temperature", "humidity", "wind_speed", "rain"]].corr().round(2))


print(
    df.groupby(["city", "rain_flag"])["pm2_5"]
    .agg(["mean", "count"])
    .round(1)
    .unstack()
)


print(
    df.groupby(["city", "wind_band"], observed=True)["pm2_5"]
    .agg(["mean", "count"])
    .round(1)
    .unstack()
)