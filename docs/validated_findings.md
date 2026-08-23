# Validated Findings — April 2026

This document records findings produced from the cleaned April 2026 Dublin Bikes dataset after Python preprocessing and SQL analysis.

## Dataset validation

- **Observations:** 617,218
- **Unique stations:** 115
- **Duplicate rows:** 0
- **Missing timestamps:** 0
- **Missing station IDs:** 0
- **Missing capacity values:** 0
- **Negative operational values flagged:** 0
- **Average bikes available per observation:** 11.94
- **Average docks available per observation:** 19.83

## Important metric definitions

`near_empty_pct` is the percentage of station-status observations where bike availability was greater than 0 but less than or equal to 10% of station capacity.

`near_full_pct` is the percentage of station-status observations where dock availability was greater than 0 but less than or equal to 10% of station capacity.

These measures identify stations at risk of becoming unusable. They do not include observations where a station was already completely empty or completely full.

## Stations most often near empty

| Rank | Station | Near-empty rate |
|---:|---|---:|
| 1 | Fitzwilliam Square East | 44.32% |
| 2 | Mountjoy Square East | 40.34% |
| 3 | Grangegorman Lower (South) | 38.39% |
| 4 | Grangegorman Lower (North) | 37.84% |
| 5 | Parnell Square North | 37.27% |
| 6 | Wilton Terrace (Park) | 37.18% |
| 7 | Hardwicke Place | 36.90% |
| 8 | Denmark Street Great | 35.27% |
| 9 | Mater Hospital | 34.58% |
| 10 | Lime Street | 33.71% |

### Interpretation

Fitzwilliam Square East showed the strongest recurring bike-shortage risk in the April 2026 extract, appearing near empty in **44.32%** of its observations. Several stations around Mountjoy Square, Grangegorman, Parnell Square and the Mater/Hardwicke area also showed high recurring near-empty rates.

These patterns indicate where rebalancing analysis should focus first, but they do not by themselves prove why bikes are being depleted. Time-of-day analysis is required before making operational recommendations.

## Stations most often near full

| Rank | Station | Near-full rate |
|---:|---|---:|
| 1 | Heuston Bridge (North) | 20.66% |
| 2 | Parkgate Street | 18.74% |
| 3 | Barrow Street | 18.30% |
| 4 | Heuston Bridge (South) | 18.13% |
| 5 | South Dock Road | 18.10% |
| 6 | Killarney Street | 17.11% |
| 7 | Fownes Street Upper | 16.10% |
| 8 | Heuston Station (Central) | 15.32% |
| 9 | Charlemont Place | 15.10% |
| 10 | Princes Street / O'Connell Street | 14.99% |

### Interpretation

Heuston Bridge (North) showed the strongest recurring dock-shortage risk, appearing near full in **20.66%** of observations. The presence of several Heuston/Parkgate stations in the top group suggests a local cluster of return-pressure risk around the Heuston area.

Barrow Street and South Dock Road also ranked highly, indicating that dock shortages are not limited to a single part of the city.

## Preliminary business implication

The April 2026 data suggests that bike rebalancing should not be treated as a uniform citywide problem. Some stations repeatedly face **bike shortages**, while others repeatedly face **dock shortages**.

The next analytical step is to identify **when** these risks occur — by hour, weekday/weekend status and peak period — before assigning rebalancing priorities.

## Caution

These findings are descriptive and month-specific. They should not be presented as permanent characteristics of a station or as proof of customer demand causality without further temporal analysis and, ideally, multiple months of data.
