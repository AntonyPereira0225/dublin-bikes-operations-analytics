# Dublin Bikes Operations Analytics

**Python | SQL | Power BI | Data Preprocessing | Operational Analytics**

## Project Overview

Dublin Bikes is a docked bike-sharing system operating across Dublin city. A station can become difficult for customers to use when it is repeatedly **empty** (no bikes available) or **full** (no docks available).

This portfolio project analyses historical Dublin Bikes station-status data to identify availability patterns, operational pressure points, and potential bike-rebalancing opportunities.

The project is designed to demonstrate an end-to-end Data Analyst workflow:

**Raw open data → Data cleaning & validation → Feature engineering → SQL analysis → Power BI dashboard → Business recommendations**

## Business Problem

> How can Dublin Bikes use historical station availability data to identify stations at risk of becoming empty or full, understand peak demand patterns, and prioritise bike-rebalancing activity?

## Business Questions

1. Which stations most frequently experience very low bike availability?
2. Which stations most frequently approach full capacity?
3. What hours and days create the greatest availability pressure?
4. How do weekday and weekend patterns differ?
5. Which stations show the strongest morning and evening demand patterns?
6. Which stations should receive the highest rebalancing priority?
7. How can these findings be communicated through an executive Power BI dashboard?

## Data Source

**Publisher:** Dublin City Council / Smart Dublin  
**Dataset:** Dublinbikes API DCC – Historical Station Data  
**Licence:** Creative Commons Attribution 4.0 (CC BY 4.0)  
**Portal:** https://data.gov.ie/en_GB/dataset/dublinbikes-api  

The source provides historical station-status observations including station identifiers, timestamps, station capacity, available bikes, available docks and location information. Raw source files are intentionally not committed to this repository; the project keeps the analysis reproducible while avoiding large raw-data files in GitHub.

## Tools & Skills Demonstrated

### Python
- Pandas
- NumPy
- Data cleaning
- Missing-value checks
- Duplicate detection
- Data-type conversion
- Feature engineering
- Data-quality validation
- Exploratory analysis

### SQL
- CTEs
- `CASE WHEN`
- Aggregations
- Date/time analysis
- Window functions
- `LAG()`
- Ranking
- Operational KPI calculations

### Power BI
- Power Query
- Data modelling
- DAX measures
- KPI cards
- Time-series analysis
- Station-level drill-down
- Geographic mapping
- Operational dashboard design

## Planned Analysis Workflow

1. Download official Dublin Bikes historical station-status data.
2. Profile the raw dataset and document data-quality issues.
3. Clean and validate station, timestamp, capacity and availability fields in Python.
4. Engineer analytical features such as hour, weekday, peak period, utilisation and availability-risk flags.
5. Export a clean analytical dataset.
6. Load the processed data into SQL and answer operational business questions.
7. Build Power BI measures and dashboard pages.
8. Summarise key findings and practical rebalancing recommendations.

## Repository Structure

```text
dublin-bikes-operations-analytics/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── README.md
├── python/
│   └── README.md
├── sql/
│   └── README.md
├── dashboard/
│   └── README.md
├── docs/
│   └── project_plan.md
└── images/
    └── README.md
```

## Project Status

🟡 **In development**

The repository structure and analytical plan are complete. Data preprocessing, SQL analysis and Power BI development will be added in the next stages.

## Author

**Antony Pereira George**  
Dublin, Ireland  
Data Analyst | SQL | Python | Power BI

---

*This project uses publicly available Dublin City Council / Smart Dublin data and is intended for educational and portfolio purposes.*
