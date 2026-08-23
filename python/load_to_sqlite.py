from pathlib import Path
import sqlite3

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEAN_CSV = PROJECT_ROOT / "data" / "processed" / "dublin_bikes_april_2026_clean.csv"
DB_PATH = PROJECT_ROOT / "data" / "dublin_bikes.db"
TABLE_NAME = "station_status"
TIMESTAMP_COLUMN = "last_reported_dublin"


def main():
    if not CLEAN_CSV.exists():
        raise FileNotFoundError(
            f"Cleaned CSV not found: {CLEAN_CSV}\n"
            "Run python/preprocess_dublin_bikes.py first."
        )

    print("Loading cleaned Dublin Bikes data...")
    df = pd.read_csv(CLEAN_CSV)

    required_columns = {TIMESTAMP_COLUMN, "station_id", "hour"}
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        raise ValueError(
            "Cleaned CSV is missing required columns: "
            + ", ".join(sorted(missing_columns))
        )

    # Standardise the Dublin-local timestamp as a sortable ISO-style text field.
    # The preprocessing step already converted source timestamps to Europe/Dublin.
    df[TIMESTAMP_COLUMN] = pd.to_datetime(
        df[TIMESTAMP_COLUMN], errors="coerce", utc=True
    ).dt.tz_convert("Europe/Dublin").dt.strftime("%Y-%m-%d %H:%M:%S%z")

    print(f"Rows to load: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql(
            TABLE_NAME,
            conn,
            if_exists="replace",
            index=False,
            chunksize=5000,
        )

        conn.execute(
            f"CREATE INDEX IF NOT EXISTS idx_station_id "
            f"ON {TABLE_NAME}(station_id)"
        )
        conn.execute(
            f"CREATE INDEX IF NOT EXISTS idx_last_reported_dublin "
            f"ON {TABLE_NAME}({TIMESTAMP_COLUMN})"
        )
        conn.execute(
            f"CREATE INDEX IF NOT EXISTS idx_station_hour "
            f"ON {TABLE_NAME}(station_id, hour)"
        )

        row_count = conn.execute(
            f"SELECT COUNT(*) FROM {TABLE_NAME}"
        ).fetchone()[0]
        station_count = conn.execute(
            f"SELECT COUNT(DISTINCT station_id) FROM {TABLE_NAME}"
        ).fetchone()[0]

    print("\nSQLite load complete")
    print("--------------------")
    print(f"Database: {DB_PATH}")
    print(f"Table: {TABLE_NAME}")
    print(f"Rows loaded: {row_count:,}")
    print(f"Unique stations: {station_count:,}")


if __name__ == "__main__":
    main()
