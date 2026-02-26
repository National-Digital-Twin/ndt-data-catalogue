-- SPDX-License-Identifier: Apache-2.0
--
-- © Crown Copyright 2025. This work has been developed by the National Digital Twin
-- Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
-- entity

-- Custom test: Assert daily reading completeness for active stations
-- This test warns if active stations don't have at least one reading per day
-- for the last 7 days

with active_stations as (
    select station_id
    from {{ ref('dim_station') }}
    where is_active = true
),

date_spine as (
    select
        date_trunc('day', current_date - interval '1 day' * generate_series(0, 6)) as check_date
),

station_dates as (
    select
        s.station_id,
        d.check_date
    from active_stations s
    cross join date_spine d
),

actual_readings as (
    select
        station_id,
        reading_date,
        count(*) as reading_count
    from {{ ref('fct_water_levels') }}
    where reading_date >= current_date - interval '7 days'
    group by station_id, reading_date
),

missing_days as (
    select
        sd.station_id,
        sd.check_date,
        coalesce(ar.reading_count, 0) as reading_count
    from station_dates sd
    left join actual_readings ar
        on sd.station_id = ar.station_id
        and sd.check_date = ar.reading_date
    where coalesce(ar.reading_count, 0) = 0
)

select
    station_id,
    check_date as missing_date,
    reading_count,
    'No readings for this active station on this date' as issue_description
from missing_days
order by station_id, check_date
