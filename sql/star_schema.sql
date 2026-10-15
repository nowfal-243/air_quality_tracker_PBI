DROP TABLE IF EXISTS fact_readings;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_city;

CREATE TABLE dim_city (
  city_id INT PRIMARY KEY AUTO_INCREMENT,
  city VARCHAR(50) NOT NULL UNIQUE,
  latitude DOUBLE,
  longitude DOUBLE
);

INSERT INTO dim_city (city, latitude, longitude)
SELECT city, MIN(latitude), MIN(longitude)
FROM air_quality_weather
GROUP BY city;

CREATE TABLE dim_date (
  date_id INT PRIMARY KEY AUTO_INCREMENT,
  full_date DATE NOT NULL UNIQUE,
  day_name VARCHAR(10),
  month_name VARCHAR(10),
  is_weekend TINYINT
);

INSERT INTO dim_date (full_date, day_name, month_name, is_weekend)
SELECT d, DAYNAME(d), MONTHNAME(d), WEEKDAY(d) >= 5
FROM (SELECT DISTINCT CAST(`date` AS DATE) AS d FROM air_quality_weather) x
ORDER BY d;

CREATE TABLE fact_readings (
  reading_id INT PRIMARY KEY AUTO_INCREMENT,
  city_id INT NOT NULL,
  date_id INT NOT NULL,
  reading_time DATETIME NOT NULL,
  hour_of_day INT,
  pm2_5 DOUBLE, pm10 DOUBLE, us_aqi INT,
  aqi_category VARCHAR(30),
  temperature DOUBLE, humidity DOUBLE, wind_speed DOUBLE, rain DOUBLE,
  rain_flag VARCHAR(10), wind_band VARCHAR(20),
  FOREIGN KEY (city_id) REFERENCES dim_city(city_id),
  FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

INSERT INTO fact_readings (city_id, date_id, reading_time, hour_of_day, pm2_5, pm10, us_aqi, aqi_category, temperature, humidity, wind_speed, rain, rain_flag, wind_band)
SELECT c.city_id, d.date_id, CAST(w.`time` AS DATETIME), w.`hour`, w.pm2_5, w.pm10, w.us_aqi, w.aqi_category, w.temperature, w.humidity, w.wind_speed, w.rain, w.rain_flag, w.wind_band
FROM air_quality_weather w
JOIN dim_city c ON c.city = w.city
JOIN dim_date d ON d.full_date = CAST(w.`date` AS DATE);