# Operational Status & Data Quality Validation

## Purpose

Before treating low bike availability or low dock availability as genuine operational pressure, the project checks whether observations were recorded while stations were active for renting and returning.

## Network-level validation

- Observations: **617,218**
- Renting active: **617,218 (100%)**
- Returning active: **617,218 (100%)**
- Capacity consistency review rows: **8,093 (~1.3%)**

This means the observed shortage/fullness patterns are **not explained by stations being unavailable for renting or returning** during the April 2026 extract.

## Priority-station validation

All Top 15 rebalancing-priority stations were active for both renting and returning in **100% of their observations**.

Examples:

- Parnell Square North: 100% renting active, 100% returning active, 0 capacity-review rows.
- Fitzwilliam Square East: 100% renting active, 100% returning active, 0 capacity-review rows.
- Heuston Bridge (North): 100% renting active, 100% returning active, 0 capacity-review rows.
- Heuston Bridge (South): 100% renting active, 100% returning active, 0 capacity-review rows.

Some stations contain a small number of capacity-consistency review rows, including James Street East (60), Wilton Terrace (Park) (51), Herbert Street (32), Hanover Quay East (24), and Mountjoy Square East (1).

## Interpretation

The rebalancing findings can therefore be treated as genuine station-availability patterns rather than simple service-outage artefacts.

The capacity-consistency flag remains a documented data-quality caveat. Because review rows represent only a small share of the full dataset, the main analysis retains them but reports the issue transparently. A future sensitivity check can compare rankings with those rows excluded.
