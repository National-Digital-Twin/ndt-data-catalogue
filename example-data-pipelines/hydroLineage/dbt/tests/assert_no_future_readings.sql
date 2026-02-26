-- SPDX-License-Identifier: Apache-2.0
--
-- © Crown Copyright 2025. This work has been developed by the National Digital Twin
-- Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
-- entity

-- Custom test: Assert that no water level readings have future timestamps
-- This test fails if any readings have timestamps after the current time

select
    reading_id,
    station_id,
    reading_timestamp,
    current_timestamp as test_run_time,
    reading_timestamp - current_timestamp as time_diff
from {{ ref('stg_water_level_readings') }}
where reading_timestamp > current_timestamp
