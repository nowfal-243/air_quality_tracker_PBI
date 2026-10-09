
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

df["rain_flag"] = (df["rain"] > 0).map({True: "Rainy", False: "Dry"})
df["wind_band"] = pd.cut(
    df["wind_speed"],
    bins=[-0.1, 5, 10, 1000],
    labels=["Calm (<5)", "Light (5-10)", "Windy (10+)"],
)

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