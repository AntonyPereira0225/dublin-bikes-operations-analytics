-- Dublin Bikes Operations Analytics
-- SQLite analysis queries
-- Table: station_status

-- 1. Network overview
SELECT
    COUNT(*) AS observations,
    COUNT(DISTINCT station_id) AS stations,
    MIN(last_reported) AS first_observation,
    MAX(last_reported) AS last_observation,
    ROUND(AVG(num_bikes_available), 2) AS avg_bikes_available,
    ROUND(AVG(num_docks_available), 2) AS avg_docks_available
FROM station_status;

-- 2. Stations most often near empty
SELECT
    station_id,
    name,
    COUNT(*) AS observations,
    SUM(CASE WHEN is_near_empty = 1 THEN 1 ELSE 0 END) AS near_empty_observations,
    ROUND(100.0 * SUM(CASE WHEN is_near_empty = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS near_empty_pct
FROM station_status
GROUP BY station_id, name
HAVING COUNT(*) >= 100
ORDER BY near_empty_pct DESC
LIMIT 15;

-- 3. Stations most often near full
SELECT
    station_id,
    name,
    COUNT(*) AS observations,
    SUM(CASE WHEN is_near_full = 1 THEN 1 ELSE 0 END) AS near_full_observations,
    ROUND(100.0 * SUM(CASE WHEN is_near_full = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS near_full_pct
FROM station_status
GROUP BY station_id, name
HAVING COUNT(*) >= 100
ORDER BY near_full_pct DESC
LIMIT 15;

-- 4. Hourly availability pressure across the network
SELECT
    hour,
    ROUND(AVG(bike_availability_pct), 2) AS avg_bike_availability_pct,
    ROUND(AVG(dock_availability_pct), 2) AS avg_dock_availability_pct,
    ROUND(100.0 * AVG(is_near_empty), 2) AS near_empty_rate_pct,
    ROUND(100.0 * AVG(is_near_full), 2) AS near_full_rate_pct
FROM station_status
GROUP BY hour
ORDER BY hour;

-- 5. Weekday vs weekend comparison
SELECT
    CASE WHEN is_weekend = 1 THEN 'Weekend' ELSE 'Weekday' END AS day_type,
    ROUND(AVG(num_bikes_available), 2) AS avg_bikes_available,
    ROUND(AVG(num_docks_available), 2) AS avg_docks_available,
    ROUND(100.0 * AVG(is_near_empty), 2) AS near_empty_rate_pct,
    ROUND(100.0 * AVG(is_near_full), 2) AS near_full_rate_pct
FROM station_status
GROUP BY day_type;

-- 6. Rebalancing priority score by station
WITH station_risk AS (
    SELECT
        station_id,
        name,
        AVG(is_near_empty) AS near_empty_rate,
        AVG(is_near_full) AS near_full_rate,
        AVG(CASE WHEN time_period = 'Morning Peak' THEN is_near_empty ELSE NULL END) AS morning_near_empty_rate,
        AVG(CASE WHEN time_period = 'Evening Peak' THEN is_near_full ELSE NULL END) AS evening_near_full_rate
    FROM station_status
    GROUP BY station_id, name
)
SELECT
    station_id,
    name,
    ROUND(100.0 * near_empty_rate, 2) AS near_empty_pct,
    ROUND(100.0 * near_full_rate, 2) AS near_full_pct,
    ROUND(100.0 * COALESCE(morning_near_empty_rate, 0), 2) AS morning_near_empty_pct,
    ROUND(100.0 * COALESCE(evening_near_full_rate, 0), 2) AS evening_near_full_pct,
    ROUND(
        100.0 * (
            0.35 * near_empty_rate +
            0.35 * near_full_rate +
            0.15 * COALESCE(morning_near_empty_rate, 0) +
            0.15 * COALESCE(evening_near_full_rate, 0)
        ),
        2
    ) AS rebalancing_priority_score
FROM station_risk
ORDER BY rebalancing_priority_score DESC
LIMIT 20;

-- 7. Rank stations by hourly bike availability
WITH hourly_station AS (
    SELECT
        station_id,
        name,
        hour,
        AVG(bike_availability_pct) AS avg_bike_availability_pct
    FROM station_status
    GROUP BY station_id, name, hour
), ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY hour
            ORDER BY avg_bike_availability_pct ASC
        ) AS availability_rank
    FROM hourly_station
)
SELECT
    hour,
    station_id,
    name,
    ROUND(avg_bike_availability_pct, 2) AS avg_bike_availability_pct,
    availability_rank
FROM ranked
WHERE availability_rank <= 5
ORDER BY hour, availability_rank;

-- 8. Detect sharp station-level changes using LAG()
WITH ordered_status AS (
    SELECT
        station_id,
        name,
        last_reported,
        num_bikes_available,
        LAG(num_bikes_available) OVER (
            PARTITION BY station_id
            ORDER BY last_reported
        ) AS previous_bikes
    FROM station_status
), changes AS (
    SELECT
        station_id,
        name,
        last_reported,
        previous_bikes,
        num_bikes_available,
        num_bikes_available - previous_bikes AS bike_change
    FROM ordered_status
    WHERE previous_bikes IS NOT NULL
)
SELECT
    station_id,
    name,
    last_reported,
    previous_bikes,
    num_bikes_available,
    bike_change
FROM changes
ORDER BY ABS(bike_change) DESC
LIMIT 50;
