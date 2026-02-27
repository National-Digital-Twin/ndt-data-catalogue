-- SPDX-License-Identifier: Apache-2.0
--
-- © Crown Copyright 2025. This work has been developed by the National Digital Twin
-- Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
-- entity

{{
    config(
        materialized='view',
        schema='analytics',
        tags=['api', 'marts']
    )
}}

with latest_readings as (
    select
        station_key,
        station_id,
        water_level_m,
        reading_timestamp,
        row_number() over (partition by station_id order by reading_timestamp desc) as rn
    from {{ ref('fct_water_levels') }}
),

stations as (
    select
        station_key,
        station_id,
        station_name,
        river_name,
        town,
        latitude,
        longitude,
        status
    from {{ ref('dim_station') }}
)

select
    s.station_id,
    s.station_name,
    s.river_name,
    s.town,
    s.latitude,
    s.longitude,
    s.status,
    r.water_level_m,
    r.reading_timestamp as last_reading_time
from stations s
left join latest_readings r 
    on s.station_key = r.station_key 
    and r.rn = 1
