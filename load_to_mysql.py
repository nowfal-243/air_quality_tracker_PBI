import pandas as pd

from db_config import get_engine

df = pd.read_csv("data/clean/air_quality_weather.csv")

engine = get_engine()
df.to_sql("air_quality_weather", engine, if_exists="replace", index=False, chunksize=5000)
print("Loaded", len(df), "rows into MySQL table air_quality_weather")
