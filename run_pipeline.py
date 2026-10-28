#!/usr/bin/env python3
"""
run_pipeline.py - Orchestrates the full air-quality-tracker pipeline.

Order:
  1. fetch_all_cities.py   - air quality data from Open-Meteo
  2. fetch_weather.py      - weather data from Open-Meteo
  3. clean_data.py         - clean & transform
  4. merge_data.py         - merge air quality + weather
  5. load_to_mysql.py      - load flat table into MySQL
  6. build_star_schema.py  - rebuild dim_city / dim_date / fact_readings

Usage:
  python run_pipeline.py                # everything
  python run_pipeline.py --skip-fetch   # reuse data/raw/*.csv (offline / API rate-limited)
  python run_pipeline.py --skip-db      # stop after merge (no MySQL needed)

Each step runs in order; the pipeline stops at the first failure.
"""
import argparse
import os
import subprocess
import sys

# Windows consoles / `| tee` use cp1252 and crash on non-ASCII characters.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

FETCH = [
    ("fetch_all_cities.py", "Fetching air quality data..."),
    ("fetch_weather.py", "Fetching weather data..."),
]
TRANSFORM = [
    ("clean_data.py", "Cleaning data..."),
    ("merge_data.py", "Merging data..."),
]
DATABASE = [
    ("load_to_mysql.py", "Loading to MySQL..."),
    ("build_star_schema.py", "Building star schema..."),
]

REQUIRED_PACKAGES = ["pandas", "requests", "sqlalchemy", "pymysql"]


def preflight(need_db):
    """Fail fast, before any API calls, if the environment is not ready."""
    missing = []
    for pkg in REQUIRED_PACKAGES:
        if pkg in ("sqlalchemy", "pymysql") and not need_db:
            continue
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"[FAILED] Missing Python packages: {', '.join(missing)}")
        print(f"         Fix: pip install {' '.join(missing)}")
        return False

    for folder in ("data/raw", "data/clean"):
        os.makedirs(os.path.join(SCRIPT_DIR, folder), exist_ok=True)

    if need_db:
        sys.path.insert(0, SCRIPT_DIR)
        try:
            from db_config import get_engine
            get_engine()  # also creates the database if it does not exist
        except SystemExit as e:
            print(f"[FAILED] MySQL check: {e}")
            return False
        print("[OK] MySQL connection works")
    return True


def run_step(script_name, description):
    print(f"\n{'=' * 60}\n  {description}\n  Running: python {script_name}\n{'=' * 60}", flush=True)

    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    proc = subprocess.Popen(
        [sys.executable, script_name],
        cwd=SCRIPT_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # keep output in the order it happened
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    for line in proc.stdout:
        print(line, end="", flush=True)
    code = proc.wait()

    if code != 0:
        print(f"\n[FAILED] {script_name} exited with code {code}")
        return False
    print(f"\n[OK] {script_name} completed")
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skip-fetch", action="store_true", help="reuse existing data/raw CSVs")
    ap.add_argument("--skip-db", action="store_true", help="stop after merge (no MySQL)")
    args = ap.parse_args()

    print("Starting Air Quality Tracker pipeline")
    print(f"  Working directory: {SCRIPT_DIR}")

    if not preflight(need_db=not args.skip_db):
        sys.exit(1)

    steps = ([] if args.skip_fetch else FETCH) + TRANSFORM + ([] if args.skip_db else DATABASE)
    for script, description in steps:
        if not run_step(script, description):
            print(f"\n{'=' * 60}\n  Pipeline stopped due to an error.\n{'=' * 60}")
            sys.exit(1)

    print(f"\n{'=' * 60}\n  All pipeline steps completed successfully!\n{'=' * 60}")


if __name__ == "__main__":
    main()
