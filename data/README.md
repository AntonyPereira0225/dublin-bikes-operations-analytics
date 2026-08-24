# Data

The project uses the official Dublin Bikes historical station-status dataset published by Dublin City Council / Smart Dublin.

## Raw source data

The large raw source file is intentionally **not committed** to GitHub. Locally, the preprocessing workflow expects:

- `data/dublin_bikes_april_2026.csv`

The source can be re-downloaded from the Dublin Bikes historical-data portal documented in the main README.

## Generated analytical data

Running `python/preprocess_dublin_bikes.py` creates:

- `data/processed/dublin_bikes_april_2026_clean.csv`

This cleaned file contains the 617,218 analysis-ready station observations used by the SQL workflow and Power BI model. It is also kept out of GitHub because of its size; the repository instead includes the full reproducible preprocessing code, SQL analysis, validated findings, dashboard screenshot and `.pbix` file.

This keeps the repository lightweight while preserving reproducibility.