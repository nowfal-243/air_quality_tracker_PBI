-- 1. Check the load
USE air_quality;
SELECT COUNT(*) FROM air_quality_readings;

-- 2. Rank cities by average AQI
SELECT city,
       ROUND(AVG(pm2_5),1) AS avg_pm25,
       ROUND(AVG(us_aqi),1) AS avg_aqi,
       RANK() OVER (ORDER BY AVG(us_aqi) DESC) AS pollution_rank
FROM air_quality_readings
GROUP BY city;

-- 3. Worst hours of the day
SELECT hour, ROUND(AVG(pm2_5),1) AS avg_pm25
FROM air_quality_readings
GROUP BY hour
ORDER BY hour;

-- 4. Share of unhealthy hours per city
SELECT city,
       SUM(us_aqi > 150) AS unhealthy_hours,
       ROUND(100 * SUM(us_aqi > 150) / COUNT(*), 1) AS pct_unhealthy
FROM air_quality_readings
GROUP BY city
ORDER BY pct_unhealthy DESC;