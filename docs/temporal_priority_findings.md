# Validated Temporal & Rebalancing Findings

This document records results produced from the April 2026 Dublin Bikes SQLite analysis.

## Network-level temporal patterns

- Near-empty risk was highest at **19:00 (17.83%)**, followed by **18:00 (17.63%)**.
- Near-full risk was highest at **21:00 (6.45%)**, with elevated levels continuing through **20:00–23:00**.
- The highest fully empty rates appeared overnight, including **03:00 (11.25%)** and **00:00 (11.24%)**.
- Fully full rates were also most elevated overnight, peaking at **02:00 (4.74%)** and **04:00 (4.73%)**.

These patterns suggest that station imbalance is not confined to commuting peaks. Evening and overnight conditions also matter for operational planning and rebalancing.

## Weekday vs weekend

| Metric | Weekday | Weekend |
|---|---:|---:|
| Average bikes available | 11.88 | 12.10 |
| Average docks available | 19.90 | 19.61 |
| Near-empty rate | 15.81% | 17.07% |
| Near-full rate | 4.84% | 6.10% |
| Empty rate | 9.74% | 7.36% |
| Full rate | 3.09% | 3.15% |

Weekend observations show higher near-empty and near-full rates, while weekday observations show a higher fully empty rate. This indicates that weekend operations may experience more stations close to capacity limits, whereas weekdays show stronger outright bike shortages at some stations.

## Highest rebalancing-priority stations

Using the project’s composite rebalancing score, the highest-ranked stations were:

1. **Parnell Square North** — 19.94
2. **Hardwicke Place** — 17.92
3. **Grangegorman Lower (North)** — 17.75
4. **Fitzwilliam Square East** — 17.52
5. **Hanover Quay East** — 16.60
6. **Heuston Bridge (South)** — 16.57
7. **Eccles Street East** — 16.51
8. **Denmark Street Great** — 16.33
9. **Merrion Square South** — 15.91
10. **Herbert Street** — 15.52

The ranking captures both bike-shortage and dock-shortage pressure. For example, Parnell Square North is dominated by bike shortages, while Heuston Bridge (South) is dominated by full-station / low-dock availability.

## Important interpretation note

The rebalancing score is a **portfolio-designed operational heuristic**, not an official Dublin Bikes KPI. It is intended to combine several risk signals into one prioritisation measure. The weighting should be presented as a transparent analytical choice and could be adjusted in a real operational setting based on service-level targets, station criticality, vehicle routing cost, and real-time demand forecasts.
