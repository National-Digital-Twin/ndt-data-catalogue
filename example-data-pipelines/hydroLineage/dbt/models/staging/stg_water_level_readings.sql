-- SPDX-License-Identifier: Apache-2.0
--
-- © Crown Copyright 2025. This work has been developed by the National Digital Twin
-- Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
-- entity

{{
    config(
        materialized='table',
        schema='staging'
    )
}}

with source as (
    select * from {{ source('raw', 'water_level_readings') }}
),

renamed as (
    select
        -- Primary key
        reading_id,
        encode(digest(coalesce(cast(reading_id as varchar), '_dbt_utils_surrogate_key_null_'), 'sha256'), 'hex') as reading_key,
        
        -- Foreign key
        station_id,
        measure_id,
        
        -- Measurement
        value as water_level_m,
        reading_datetime::timestamp as reading_timestamp,
        
        -- Time dimensions
        date(reading_datetime::timestamp) as reading_date,
        extract(hour from reading_datetime::timestamp) as reading_hour,
        
        -- Data quality flags
        case 
            when value < -10.0 or value > 50.0 then true
            else false
        end as is_outlier,
        
        case
            when reading_datetime::timestamp > current_timestamp then true
            else false
        end as is_future_reading,
        
        -- Measure reference
        measure_id as measure_uri,
        
        -- Metadata
        "_airbyte_extracted_at" as airbyte_extracted_at,
        row_number() over (partition by reading_id order by "_airbyte_extracted_at" desc) as row_num
    from source
    where reading_datetime::timestamp <= current_timestamp  -- Filter out future readings
),

final as (
    select
        reading_key,
        reading_id,
        station_id,
        reading_timestamp,
        water_level_m,
        reading_date,
        reading_hour,
        is_outlier,
        is_future_reading,
        measure_uri,
        airbyte_extracted_at
    from renamed
    where row_num = 1
)

select * from final
