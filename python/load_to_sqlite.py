from pathlib import Path
import sqlite3
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEAN_CSV = PROJECT_ROOT / "data" / "processed" / "dublin_bikes_april_2026_clean.csv"
DB_PATH = PROJECT_ROOT / "data" / "dublin_bikes.db"
TABLE_NAME = "station_status"


def main():
    if not CLEAN_CSV.exists():
        raise FileNotFoundError(
            f"Cleaned CSV not found: {CLEAN_CSV}\n"
            "Run python/preprocess_dublin_bikes.py first."
        )

    print("Loading cleaned Dublin Bikes data...")
    df = pd.read_csv(CLEAN_CSV)

    # Store datetime as an ISO-like string so SQLite date/time functions remain usable.
    if "last_reported" in df.columns:
        df["last_reported"] = pd.to_datetime(df["last_reported"], errors="coerce").dt.strftime("%Y-%m-%d %H:%M:%S")

    print(f"Rows to load: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False, chunksize=5000)

        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_station_id ON {TABLE_NAME}(station_id)")
        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_last_reported ON {TABLE_NAME}(last_reported)")
        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_station_hour ON {TABLE_NAME}(station_id, hour)")

        row_count = conn.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()[0]
        station_count = conn.execute(f"SELECT COUNT(DISTINCT station_id) FROM {TABLE_NAME}").fetchone()[0]

    print("\nSQLite load complete")
    print("--------------------")
    print(f"Database: {DB_PATH}")
    print(f"Table: {TABLE_NAME}")
    print(f"Rows loaded: {row_count:,}")
    print(f"Unique stations: {station_count:,}")


if __name__ == "__main__":
    main()
