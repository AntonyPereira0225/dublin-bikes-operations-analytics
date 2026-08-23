# Dublin Bikes Data Dictionary

Source: Dublin City Council / Smart Dublin historical station-status data.

For the first analysis stage, this project uses **April 2026** historical station data because the official resource includes a complete published schema and more than 600,000 observations.

## Fields

| Column | Type | Meaning in this project |
|---|---|---|
| `system_id` | text | Bike-share system identifier. |
| `last_reported` | timestamp | Timestamp when the station status was reported. This is the key time field for hourly/day-of-week analysis. |
| `station_id` | numeric | Unique station identifier. |
| `num_bikes_available` | numeric | Number of bikes available to rent at the station at that observation. |
| `num_docks_available` | numeric | Number of empty docks available for returned bikes. |
| `is_installed` | text | Indicates whether the station is installed/active in the system feed. |
| `is_renting` | text | Indicates whether users can rent bikes from the station. |
| `is_returning` | text | Indicates whether users can return bikes to the station. |
| `name` | text | Station name. |
| `short_name` | text | Short station identifier/name used in the source feed. |
| `address` | text | Station address. |
| `lat` | numeric | Station latitude. |
| `lon` | numeric | Station longitude. |
| `region_id` | text | Region identifier from the feed, where populated. |
| `capacity` | numeric | Total docking capacity of the station. |

## Core analytical fields

The main fields used for the business analysis will be:

- `last_reported`
- `station_id`
- `name`
- `num_bikes_available`
- `num_docks_available`
- `capacity`
- `lat`
- `lon`
- `is_renting`
- `is_returning`

## Features we will create in Python

The raw dataset will be transformed into additional analytical fields such as:

- `date`
- `hour`
- `day_name`
- `is_weekend`
- `time_period`
- `bike_availability_pct`
- `dock_availability_pct`
- `is_empty`
- `is_near_empty`
- `is_full`
- `is_near_full`
- `rebalancing_risk`

These derived fields will allow us to analyse station pressure, peak periods, availability risk and operational rebalancing priorities.

## Source note

Official dataset page: https://data.gov.ie/en_GB/dataset/dublinbikes-api

April 2026 resource: `Dublin Bikes Historical Station Data April 2026`.

Licence: **Creative Commons Attribution 4.0 (CC BY 4.0)**.
