from pathlib import Path
import sqlite3

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "dublin_bikes.db"

HOURLY_QUERY = """
SELECT
    hour,
    ROUND(AVG(bike_availability_pct) * 100.0, 2) AS avg_bike_availability_pct,
    ROUND(AVG(dock_availability_pct) * 100.0, 2) AS avg_dock_availability_pct,
    ROUND(100.0 * AVG(is_near_empty), 2) AS near_empty_rate_pct,
    ROUND(100.0 * AVG(is_near_full), 2) AS near_full_rate_pct,
    ROUND(100.0 * AVG(is_empty), 2) AS empty_rate_pct,
    ROUND(100.0 * AVG(is_full), 2) AS full_rate_pct
FROM station_status
GROUP BY hour
ORDER BY hour;
"""

DAY_TYPE_QUERY = """
SELECT
    CASE WHEN is_weekend = 1 THEN 'Weekend' ELSE 'Weekday' END AS day_type,
    ROUND(AVG(num_bikes_available), 2) AS avg_bikes_available,
    ROUND(AVG(num_docks_available), 2) AS avg_docks_available,
    ROUND(100.0 * AVG(is_near_empty), 2) AS near_empty_rate_pct,
    ROUND(100.0 * AVG(is_near_full), 2) AS near_full_rate_pct,
    ROUND(100.0 * AVG(is_empty), 2) AS empty_rate_pct,
    ROUND(100.0 * AVG(is_full), 2) AS full_rate_pct
FROM station_status
GROUP BY day_type
ORDER BY day_type;
"""

PRIORITY_QUERY = """
WITH station_risk AS (
    SELECT
        station_id,
        name,
        COUNT(*) AS observations,
        AVG(is_empty) AS empty_rate,
        AVG(is_near_empty) AS near_empty_rate,
        AVG(is_full) AS full_rate,
        AVG(is_near_full) AS near_full_rate,
        AVG(CASE WHEN time_period = 'Morning Peak' THEN is_empty ELSE NULL END) AS morning_empty_rate,
        AVG(CASE WHEN time_period = 'Morning Peak' THEN is_near_empty ELSE NULL END) AS morning_near_empty_rate,
        AVG(CASE WHEN time_period = 'Evening Peak' THEN is_full ELSE NULL END) AS evening_full_rate,
        AVG(CASE WHEN time_period = 'Evening Peak' THEN is_near_full ELSE NULL END) AS evening_near_full_rate
    FROM station_status
    GROUP BY station_id, name
), scored AS (
    SELECT
        station_id,
        name,
        observations,
        100.0 * empty_rate AS empty_pct,
        100.0 * near_empty_rate AS near_empty_pct,
        100.0 * full_rate AS full_pct,
        100.0 * near_full_rate AS near_full_pct,
        100.0 * (
            0.25 * empty_rate +
            0.20 * near_empty_rate +
            0.25 * full_rate +
            0.20 * near_full_rate +
            0.05 * COALESCE(morning_empty_rate + morning_near_empty_rate, 0) +
            0.05 * COALESCE(evening_full_rate + evening_near_full_rate, 0)
        ) AS priority_score
    FROM station_risk
)
SELECT
    station_id,
    name,
    observations,
    ROUND(empty_pct, 2) AS empty_pct,
    ROUND(near_empty_pct, 2) AS near_empty_pct,
    ROUND(full_pct, 2) AS full_pct,
    ROUND(near_full_pct, 2) AS near_full_pct,
    ROUND(priority_score, 2) AS rebalancing_priority_score
FROM scored
ORDER BY rebalancing_priority_score DESC
LIMIT 15;
"""


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"SQLite database not found: {DB_PATH}\n"
            "Run python/load_to_sqlite.py first."
        )

    with sqlite3.connect(DB_PATH) as conn:
        hourly = pd.read_sql_query(HOURLY_QUERY, conn)
        day_type = pd.read_sql_query(DAY_TYPE_QUERY, conn)
        priority = pd.read_sql_query(PRIORITY_QUERY, conn)

    print("Hourly network availability risk")
    print("--------------------------------")
    print(hourly.to_string(index=False))

    print("\nWeekday vs weekend")
    print("------------------")
    print(day_type.to_string(index=False))

    print("\nTop 15 rebalancing-priority stations")
    print("------------------------------------")
    print(priority.to_string(index=False))


if __name__ == "__main__":
    main()
