"""Small helper: GET a JSON endpoint with timeout + retries (Open-Meteo rate-limits)."""
import time

import requests


def get_json(url, params, retries=4, timeout=60):
    last = None
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(url, params=params, timeout=timeout)
            data = r.json()
            if r.ok and "hourly" in data:
                return data
            last = data.get("reason") or f"HTTP {r.status_code}"
        except (requests.RequestException, ValueError) as e:
            last = str(e)
        if attempt < retries:
            wait = 15 * attempt
            print(f"  API problem ({last}); retry {attempt}/{retries - 1} in {wait}s")
            time.sleep(wait)
    raise SystemExit(f"API request failed after {retries} tries: {last}\nURL: {url}")
