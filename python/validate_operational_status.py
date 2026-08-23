from pathlib import Path
import sqlite3

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "dublin_bikes.db"

NETWORK_STATUS_QUERY = """
SELECT
    COUNT(*) AS observations,
    SUM(CASE WHEN CAST(is_renting AS TEXT) IN ('1', 'True', 'true') THEN 1 ELSE 0 END) AS renting_active,
    SUM(CASE WHEN CAST(is_returning AS TEXT) IN ('1', 'True', 'true') THEN 1 ELSE 0 END) AS returning_active,
    SUM(CASE WHEN capacity_consistency_flag = 'Review' THEN 1 ELSE 0 END) AS capacity_review_rows
FROM station_status;
"""

STATION_STATUS_QUERY = """
SELECT
    station_id,
    name,
    COUNT(*) AS observations,
    ROUND(
        100.0 * AVG(CASE WHEN CAST(is_renting AS TEXT) IN ('1', 'True', 'true') THEN 1.0 ELSE 0.0 END),
        2
    ) AS renting_active_pct,
    ROUND(
        100.0 * AVG(CASE WHEN CAST(is_returning AS TEXT) IN ('1', 'True', 'true') THEN 1.0 ELSE 0.0 END),
        2
    ) AS returning_active_pct,
    ROUND(100.0 * AVG(is_empty), 2) AS empty_pct,
    ROUND(100.0 * AVG(is_near_empty), 2) AS near_empty_pct,
    ROUND(100.0 * AVG(is_full), 2) AS full_pct,
    ROUND(100.0 * AVG(is_near_full), 2) AS near_full_pct
FROM station_status
GROUP BY station_id, name
ORDER BY renting_active_pct ASC, returning_active_pct ASC, observations DESC;
"""

PRIORITY_STATIONS_QUERY = """
WITH priority_ids(station_id) AS (
    VALUES (30), (61), (105), (89), (117), (100), (79), (59), (113), (47), (114), (92), (111), (37), (20)
)
SELECT
    s.station_id,
    s.name,
    COUNT(*) AS observations,
    ROUND(
        100.0 * AVG(CASE WHEN CAST(s.is_renting AS TEXT) IN ('1', 'True', 'true') THEN 1.0 ELSE 0.0 END),
        2
    ) AS renting_active_pct,
    ROUND(
        100.0 * AVG(CASE WHEN CAST(s.is_returning AS TEXT) IN ('1', 'True', 'true') THEN 1.0 ELSE 0.0 END),
        2
    ) AS returning_active_pct,
    SUM(CASE WHEN s.capacity_consistency_flag = 'Review' THEN 1 ELSE 0 END) AS capacity_review_rows
FROM station_status s
JOIN priority_ids p ON s.station_id = p.station_id
GROUP BY s.station_id, s.name
ORDER BY s.station_id;
"""


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"SQLite database not found: {DB_PATH}\n"
            "Run python/load_to_sqlite.py first."
        )

    with sqlite3.connect(DB_PATH) as conn:
        network = pd.read_sql_query(NETWORK_STATUS_QUERY, conn)
        station_status = pd.read_sql_query(STATION_STATUS_QUERY, conn)
        priority_status = pd.read_sql_query(PRIORITY_STATIONS_QUERY, conn)

    print("Network operational-status validation")
    print("-------------------------------------")
    print(network.to_string(index=False))

    print("\nTop 15 priority stations - service status")
    print("-----------------------------------------")
    print(priority_status.to_string(index=False))

    print("\nStations with lowest renting/returning availability")
    print("---------------------------------------------------")
    print(station_status.head(15).to_string(index=False))


if __name__ == "__main__":
    main()
