<img width="1227" height="695" alt="image" src="https://github.com/user-attachments/assets/80bb7280-6d99-4918-bc2c-62132627aabf" />
# Air Quality Tracker (India)

Tracks and compares air quality and weather across 10 Indian cities.

## Tech Stack
Python (pandas, requests) | MySQL | Excel | Power BI

## Pipeline
Open-Meteo API → Python (fetch, clean, merge) → MySQL → Power BI

## Key Findings
1. Delhi had the worst air (avg AQI 153.4, PM2.5 60.9 µg/m³) and Tirunelveli the best (AQI 43.3, PM2.5 8.7), so Delhi's average AQI was about 3.5x Tirunelveli's. Lucknow (101.6) and Kolkata (91.1) ranked 2nd and 3rd.
2. Wind speed had the clearest effect on PM2.5. In all 10 cities, windy hours (10+ km/h) had lower PM2.5 than calm hours (<5 km/h), by about 48% on average (r = -0.49 pooled).
3. Rainy hours had lower PM2.5 than dry hours in 8 of 10 cities, by about 28% on average within cities (up to 52% in Mumbai and Kolkata). Chennai and Tirunelveli, two of the cleanest cities, showed no decrease.
## Dashboard
## Dashboard
![Air Quality Tracker](powerbi/Tracker.png)


## Limitations
- Analysis covers 91 days (21,840 hourly rows across 10 cities), mostly monsoon season, so rain and wind effects are mixed with seasonal change
- Time of day is not controlled for, so part of the wind effect may be the daily cycle
- Associations only, not proof of cause

## How to Run
1. python fetch_all_cities.py
2. python fetch_weather.py
3. python clean_data.py
4. python merge_data.py
5. python load_to_mysql.py
6. Open powerbi/air_quality_dashboard.pbix