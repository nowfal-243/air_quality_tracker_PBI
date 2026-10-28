-- Run after the pipeline (load_to_mysql.py + build_star_schema.py).
USE air_quality;

-- 1. Check the load
SELECT COUNT(*) AS flat_rows FROM air_quality_weather;
SELECT COUNT(*) AS fact_rows FROM fact_readings;

-- 2. Rank cities by average AQI
SELECT c.city,
       ROUND(AVG(f.pm2_5),1) AS avg_pm25,
       ROUND(AVG(f.us_aqi),1) AS avg_aqi,
       RANK() OVER (ORDER BY AVG(f.us_aqi) DESC) AS pollution_rank
FROM fact_readings f
JOIN dim_city c ON c.city_id = f.city_id
GROUP BY c.city;

-- 3. Worst hours of the day
SELECT hour_of_day, ROUND(AVG(pm2_5),1) AS avg_pm25
FROM fact_readings
GROUP BY hour_of_day
ORDER BY hour_of_day;

-- 4. Share of unhealthy hours per city
SELECT c.city,
       SUM(f.us_aqi > 150) AS unhealthy_hours,
       ROUND(100 * SUM(f.us_aqi > 150) / COUNT(*), 1) AS pct_unhealthy
FROM fact_readings f
JOIN dim_city c ON c.city_id = f.city_id
GROUP BY c.city
ORDER BY pct_unhealthy DESC;
