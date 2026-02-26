-- SPDX-License-Identifier: Apache-2.0
--
-- © Crown Copyright 2025. This work has been developed by the National Digital Twin
-- Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
-- entity

{{
    config(
        materialized='incremental',
        schema='analytics',
        unique_key='reading_key',
        on_schema_change='append_new_columns',
        tags=['fact', 'core']
    )
}}

with readings as (
    select * from {{ ref('stg_water_level_readings') }}
    
    {% if is_incremental() %}
    -- Only process new readings since last run
    where reading_timestamp > (select coalesce(max(reading_timestamp), '1900-01-01'::timestamp) from {{ this }})
    {% endif %}
),

stations as (
    select 
        station_key,
        station_id
    from {{ ref('dim_station') }}
),

joined as (
    select
        -- Keys
        readings.reading_key,
        stations.station_key,
        readings.station_id,
        
        -- Time dimensions
        readings.reading_timestamp,
        readings.reading_date,
        readings.reading_hour,
        
        -- Measurements
        readings.water_level_m,
        readings.is_outlier,
        
        -- References
        readings.measure_uri,
        
        -- Metadata
        readings.airbyte_extracted_at as source_updated_at,
        current_timestamp as dbt_updated_at
        
    from readings
    left join stations on readings.station_id = stations.station_id
)

select * from joined
