import pandas as pd

df = pd.read_csv("data/raw/all_cities.csv")

# 1. Fix the time column and add date/hour
df["time"] = pd.to_datetime(df["time"])
df["date"] = df["time"].dt.date
df["hour"] = df["time"].dt.hour

# 2. Remove rows with no data
df = df.dropna(subset=["pm2_5", "us_aqi"])

# 3. Remove duplicates
df = df.drop_duplicates(subset=["city", "time"])

# 4. Add AQI category
def category(aqi):
    if aqi <= 50: return "Good"
    elif aqi <= 100: return "Moderate"
    elif aqi <= 150: return "Unhealthy for Sensitive"
    elif aqi <= 200: return "Unhealthy"
    elif aqi <= 300: return "Very Unhealthy"
    else: return "Hazardous"

df["aqi_category"] = df["us_aqi"].apply(category)

df.to_csv("data/clean/air_quality_clean.csv", index=False)
print(df.shape)
print(df["aqi_category"].value_counts())