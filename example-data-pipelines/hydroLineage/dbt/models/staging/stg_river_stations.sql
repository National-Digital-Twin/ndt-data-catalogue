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
    select * from {{ source('raw', 'stations') }}
),

renamed as (
    select
        -- Primary key
        "notation" as station_id,
        
        -- Station information
        "label" as station_name,
        "stationReference" as station_reference,
        "wiskiID" as wiski_id,
        "riverName" as river_name,
        "town",
        "catchmentName" as catchment_name,
        "status",
        "dateOpened" as date_opened,
        
        -- Geographic coordinates
        "lat" as latitude,
        "long" as longitude,
        "easting",
        "northing",
        
        -- Metadata
        "_id" as airbyte_id,
        "_airbyte_extracted_at" as airbyte_extracted_at,
        row_number() over (partition by "notation" order by "_airbyte_extracted_at" desc) as row_num
    from source
),

-- Deduplicate: keep most recent record per station_id
deduplicated as (
    select
        station_id,
        station_name,
        station_reference,
        wiski_id,
        river_name,
        town,
        catchment_name,
        status,
        date_opened,
        latitude,
        longitude,
        easting,
        northing,
        airbyte_id,
        airbyte_extracted_at
    from renamed
    where row_num = 1
)

select * from deduplicated
