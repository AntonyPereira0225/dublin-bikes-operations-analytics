from pathlib import Path
import sqlite3

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "dublin_bikes.db"

NEAR_EMPTY_QUERY = """
SELECT
    station_id,
    name,
    COUNT(*) AS observations,
    SUM(CASE WHEN is_near_empty = 1 THEN 1 ELSE 0 END) AS near_empty_observations,
    ROUND(
        100.0 * SUM(CASE WHEN is_near_empty = 1 THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS near_empty_pct
FROM station_status
GROUP BY station_id, name
HAVING COUNT(*) >= 100
ORDER BY near_empty_pct DESC
LIMIT 10;
"""

NEAR_FULL_QUERY = """
SELECT
    station_id,
    name,
    COUNT(*) AS observations,
    SUM(CASE WHEN is_near_full = 1 THEN 1 ELSE 0 END) AS near_full_observations,
    ROUND(
        100.0 * SUM(CASE WHEN is_near_full = 1 THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS near_full_pct
FROM station_status
GROUP BY station_id, name
HAVING COUNT(*) >= 100
ORDER BY near_full_pct DESC
LIMIT 10;
"""


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"SQLite database not found: {DB_PATH}\n"
            "Run python/load_to_sqlite.py first."
        )

    with sqlite3.connect(DB_PATH) as conn:
        near_empty = pd.read_sql_query(NEAR_EMPTY_QUERY, conn)
        near_full = pd.read_sql_query(NEAR_FULL_QUERY, conn)

    print("Top 10 stations most often near empty")
    print("-------------------------------------")
    print(near_empty.to_string(index=False))

    print("\nTop 10 stations most often near full")
    print("------------------------------------")
    print(near_full.to_string(index=False))


if __name__ == "__main__":
    main()
