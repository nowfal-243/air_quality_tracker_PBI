"""Rebuild dim_city / dim_date / fact_readings from air_quality_weather.

Runs sql/star_schema.sql one statement at a time (the MySQL driver cannot run
several statements in one call). Run after load_to_mysql.py so Power BI sees fresh data.
"""
import os

from sqlalchemy import text

from db_config import BASE_DIR, get_engine

sql_path = os.path.join(BASE_DIR, "sql", "star_schema.sql")
with open(sql_path, "r", encoding="utf-8") as f:
    statements = [s.strip() for s in f.read().split(";") if s.strip()]

engine = get_engine()
with engine.begin() as conn:
    for stmt in statements:
        conn.execute(text(stmt))
    for table in ("dim_city", "dim_date", "fact_readings"):
        n = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
        print(f"{table}: {n} rows")
