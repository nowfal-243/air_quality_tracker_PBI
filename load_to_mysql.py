import pandas as pd
from getpass import getpass
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

password = getpass("MySQL root password: ")

df = pd.read_csv("data/clean/air_quality_weather.csv")

url = URL.create(
    "mysql+pymysql",
    username="root",
    password=password,
    host="127.0.0.1",
    port=3306,
    database="air_quality",
)
engine = create_engine(url)

df.to_sql("air_quality_weather", engine, if_exists="replace", index=False)
print("Loaded", len(df), "rows into MySQL")