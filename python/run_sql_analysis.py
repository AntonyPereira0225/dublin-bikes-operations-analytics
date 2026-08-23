from pathlib import Path
import sqlite3

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "dublin_bikes.db"

NETWORK_OVERVIEW_QUERY = """
SELECT
    COUNT(*) AS observations,
    COUNT(DISTINCT station_id) AS stations,
    MIN(last_reported_dublin) AS first_observation,
    MAX(last_reported_dublin) AS last_observation,
    ROUND(AVG(num_bikes_available), 2) AS avg_bikes_available,
    ROUND(AVG(num_docks_available), 2) AS avg_docks_available
FROM station_status;
"""


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"SQLite database not found: {DB_PATH}\n"
            "Run python/load_to_sqlite.py first."
        )

    with sqlite3.connect(DB_PATH) as conn:
        result = pd.read_sql_query(NETWORK_OVERVIEW_QUERY, conn)

    print("Dublin Bikes - SQL Network Overview")
    print("-----------------------------------")
    print(result.to_string(index=False))


if __name__ == "__main__":
    main()
