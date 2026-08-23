from pathlib import Path
import sqlite3

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "dublin_bikes.db"
IMAGES_DIR = PROJECT_ROOT / "images"

HOURLY_QUERY = """
SELECT
    hour,
    ROUND(100.0 * AVG(is_near_empty), 2) AS near_empty_rate_pct,
    ROUND(100.0 * AVG(is_near_full), 2) AS near_full_rate_pct,
    ROUND(100.0 * AVG(is_empty), 2) AS empty_rate_pct,
    ROUND(100.0 * AVG(is_full), 2) AS full_rate_pct
FROM station_status
GROUP BY hour
ORDER BY hour;
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
        AVG(CASE WHEN time_period = 'Morning Peak' THEN is_near_empty ELSE NULL END) AS morning_near_empty_rate,
        AVG(CASE WHEN time_period = 'Evening Peak' THEN is_near_full ELSE NULL END) AS evening_near_full_rate
    FROM station_status
    GROUP BY station_id, name
), scored AS (
    SELECT
        station_id,
        name,
        observations,
        100.0 * (
            0.25 * empty_rate +
            0.20 * near_empty_rate +
            0.25 * full_rate +
            0.20 * near_full_rate +
            0.05 * COALESCE(morning_near_empty_rate, 0) +
            0.05 * COALESCE(evening_near_full_rate, 0)
        ) AS rebalancing_priority_score
    FROM station_risk
)
SELECT
    station_id,
    name,
    observations,
    ROUND(rebalancing_priority_score, 2) AS rebalancing_priority_score
FROM scored
ORDER BY rebalancing_priority_score DESC
LIMIT 10;
"""


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"SQLite database not found: {DB_PATH}\n"
            "Run python/load_to_sqlite.py first."
        )

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        hourly = pd.read_sql_query(HOURLY_QUERY, conn)
        priority = pd.read_sql_query(PRIORITY_QUERY, conn)

    # Chart 1: hourly near-empty and near-full risk.
    plt.figure(figsize=(10, 6))
    plt.plot(hourly["hour"], hourly["near_empty_rate_pct"], marker="o", label="Near empty")
    plt.plot(hourly["hour"], hourly["near_full_rate_pct"], marker="o", label="Near full")
    plt.title("Dublin Bikes: Hourly Station Availability Risk")
    plt.xlabel("Hour of day")
    plt.ylabel("Share of observations (%)")
    plt.xticks(range(0, 24))
    plt.legend()
    plt.tight_layout()
    hourly_path = IMAGES_DIR / "hourly_availability_risk.png"
    plt.savefig(hourly_path, dpi=160)
    plt.close()

    # Chart 2: top rebalancing-priority stations.
    priority_plot = priority.sort_values("rebalancing_priority_score")
    plt.figure(figsize=(10, 7))
    plt.barh(priority_plot["name"], priority_plot["rebalancing_priority_score"])
    plt.title("Top 10 Dublin Bikes Rebalancing-Priority Stations")
    plt.xlabel("Rebalancing priority score")
    plt.ylabel("Station")
    plt.tight_layout()
    priority_path = IMAGES_DIR / "top_rebalancing_priority_stations.png"
    plt.savefig(priority_path, dpi=160)
    plt.close()

    print("Portfolio visuals created")
    print("-------------------------")
    print(f"Saved: {hourly_path}")
    print(f"Saved: {priority_path}")


if __name__ == "__main__":
    main()
