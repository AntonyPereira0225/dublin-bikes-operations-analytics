from pathlib import Path

import numpy as np
import pandas as pd


# -----------------------------------------------------------------------------
# File paths
# -----------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = PROJECT_ROOT / "data" / "dublin_bikes_april_2026.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_FILE = PROCESSED_DIR / "dublin_bikes_april_2026_clean.csv"


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
REQUIRED_COLUMNS = [
    "last_reported",
    "station_id",
    "num_bikes_available",
    "num_docks_available",
    "name",
    "lat",
    "lon",
    "capacity",
]


# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------
def classify_time_period(hour: int) -> str:
    """Convert hour of day into a simple operational time period."""
    if 6 <= hour < 10:
        return "Morning Peak"
    if 10 <= hour < 16:
        return "Midday"
    if 16 <= hour < 20:
        return "Evening Peak"
    return "Off Peak"


def classify_rebalancing_risk(row: pd.Series) -> str:
    """Assign an operational risk label from bike/dock availability percentages."""
    if row["is_empty"] == 1 or row["is_full"] == 1:
        return "Critical"
    if row["is_near_empty"] == 1 or row["is_near_full"] == 1:
        return "High"
    return "Normal"


# -----------------------------------------------------------------------------
# Main preprocessing pipeline
# -----------------------------------------------------------------------------
def main() -> None:
    print("Loading Dublin Bikes raw data...")

    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Raw file not found: {RAW_FILE}\n"
            "Make sure the CSV is named 'dublin_bikes_april_2026.csv' "
            "and placed inside the local data folder."
        )

    df = pd.read_csv(RAW_FILE, low_memory=False)

    print(f"Raw rows: {len(df):,}")
    print(f"Raw columns: {len(df.columns):,}")

    # -------------------------------------------------------------------------
    # 1. Validate expected schema
    # -------------------------------------------------------------------------
    missing_required = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_required:
        raise ValueError(
            "The dataset is missing required columns: " + ", ".join(missing_required)
        )

    # -------------------------------------------------------------------------
    # 2. Standardise data types
    # -------------------------------------------------------------------------
    df["last_reported"] = pd.to_datetime(df["last_reported"], errors="coerce", utc=True)

    numeric_columns = [
        "station_id",
        "num_bikes_available",
        "num_docks_available",
        "lat",
        "lon",
        "capacity",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # -------------------------------------------------------------------------
    # 3. Basic data-quality checks
    # -------------------------------------------------------------------------
    duplicate_rows = int(df.duplicated().sum())
    missing_timestamps = int(df["last_reported"].isna().sum())
    missing_station_ids = int(df["station_id"].isna().sum())
    missing_capacity = int(df["capacity"].isna().sum())

    print("\nData-quality profile")
    print("--------------------")
    print(f"Duplicate rows: {duplicate_rows:,}")
    print(f"Missing timestamps: {missing_timestamps:,}")
    print(f"Missing station IDs: {missing_station_ids:,}")
    print(f"Missing capacity values: {missing_capacity:,}")

    # Remove exact duplicates and observations that cannot be used analytically.
    df = df.drop_duplicates().copy()
    df = df.dropna(subset=["last_reported", "station_id", "name", "capacity"]).copy()

    # Capacity must be positive for percentage calculations.
    df = df[df["capacity"] > 0].copy()

    # -------------------------------------------------------------------------
    # 4. Operational consistency checks
    # -------------------------------------------------------------------------
    df["reported_total_slots"] = (
        df["num_bikes_available"].fillna(0) + df["num_docks_available"].fillna(0)
    )

    df["capacity_difference"] = df["reported_total_slots"] - df["capacity"]
    df["capacity_consistency_flag"] = np.where(
        df["capacity_difference"].abs() <= 1,
        "Consistent",
        "Review",
    )

    # -------------------------------------------------------------------------
    # 5. Feature engineering
    # -------------------------------------------------------------------------
    # Convert to Dublin-local time for operational analysis.
    df["last_reported_dublin"] = df["last_reported"].dt.tz_convert("Europe/Dublin")

    df["date"] = df["last_reported_dublin"].dt.date
    df["hour"] = df["last_reported_dublin"].dt.hour
    df["day_name"] = df["last_reported_dublin"].dt.day_name()
    df["day_of_week"] = df["last_reported_dublin"].dt.dayofweek
    df["is_weekend"] = np.where(df["day_of_week"] >= 5, 1, 0)
    df["time_period"] = df["hour"].apply(classify_time_period)

    df["bike_availability_pct"] = (
        df["num_bikes_available"] / df["capacity"]
    ).clip(lower=0, upper=1)

    df["dock_availability_pct"] = (
        df["num_docks_available"] / df["capacity"]
    ).clip(lower=0, upper=1)

    # Operational thresholds for this portfolio analysis.
    df["is_empty"] = np.where(df["num_bikes_available"] <= 0, 1, 0)
    df["is_near_empty"] = np.where(
        (df["bike_availability_pct"] > 0)
        & (df["bike_availability_pct"] <= 0.10),
        1,
        0,
    )

    df["is_full"] = np.where(df["num_docks_available"] <= 0, 1, 0)
    df["is_near_full"] = np.where(
        (df["dock_availability_pct"] > 0)
        & (df["dock_availability_pct"] <= 0.10),
        1,
        0,
    )

    df["rebalancing_risk"] = df.apply(classify_rebalancing_risk, axis=1)

    # -------------------------------------------------------------------------
    # 6. Final analytical validation
    # -------------------------------------------------------------------------
    impossible_negative_values = int(
        (
            (df["num_bikes_available"] < 0)
            | (df["num_docks_available"] < 0)
            | (df["capacity"] < 0)
        ).sum()
    )

    print(f"Negative operational values flagged: {impossible_negative_values:,}")

    # Keep useful analysis fields in a clear order.
    preferred_columns = [
        "last_reported_dublin",
        "date",
        "hour",
        "day_name",
        "day_of_week",
        "is_weekend",
        "time_period",
        "station_id",
        "name",
        "address",
        "lat",
        "lon",
        "capacity",
        "num_bikes_available",
        "num_docks_available",
        "bike_availability_pct",
        "dock_availability_pct",
        "is_empty",
        "is_near_empty",
        "is_full",
        "is_near_full",
        "rebalancing_risk",
        "reported_total_slots",
        "capacity_difference",
        "capacity_consistency_flag",
        "is_renting",
        "is_returning",
    ]

    final_columns = [col for col in preferred_columns if col in df.columns]
    clean_df = df[final_columns].copy()

    # -------------------------------------------------------------------------
    # 7. Save processed dataset
    # -------------------------------------------------------------------------
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    clean_df.to_csv(PROCESSED_FILE, index=False)

    print("\nPreprocessing complete")
    print("----------------------")
    print(f"Clean rows: {len(clean_df):,}")
    print(f"Unique stations: {clean_df['station_id'].nunique():,}")
    print(f"Date range: {clean_df['date'].min()} to {clean_df['date'].max()}")
    print(f"Saved to: {PROCESSED_FILE}")


if __name__ == "__main__":
    main()
