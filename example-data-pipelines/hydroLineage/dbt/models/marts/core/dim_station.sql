-- SPDX-License-Identifier: Apache-2.0
--
-- © Crown Copyright 2025. This work has been developed by the National Digital Twin
-- Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
-- entity

{{
    config(
        materialized='table',
        schema='analytics',
        tags=['dimension', 'core']
    )
}}

with stations as (
    select * from {{ ref('stg_river_stations') }}
),

enriched as (
    select
        -- Surrogate key (SHA256 - PostgreSQL 18 doesn't support MD5 without OpenSSL)
        encode(digest(coalesce(cast(station_id as varchar), '_dbt_utils_surrogate_key_null_'), 'sha256'), 'hex') as station_key,
        
        -- Natural key
        station_id,
        
        -- Station attributes
        station_name,
        station_reference,
        wiski_id,
        river_name,
        town,
        catchment_name,
        status,
        date_opened,
        
        -- Geographic attributes
        latitude,
        longitude,
        easting,
        northing,
        
        -- Derived attributes
        case 
            when status = 'Active' then true
            else false
        end as is_active,
        
        case
            when latitude >= 54.0 then 'North'
            when latitude >= 52.0 then 'Central'
            else 'South'
        end as region,
        
        -- Metadata
        airbyte_extracted_at as source_updated_at,
        current_timestamp as dbt_updated_at
        
    from stations
)

select * from enriched
