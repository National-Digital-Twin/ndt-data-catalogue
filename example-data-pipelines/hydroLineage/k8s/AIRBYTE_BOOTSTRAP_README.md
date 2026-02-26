<!--
SPDX-License-Identifier: Apache-2.0

© Crown Copyright 2025. This work has been developed by the National Digital Twin
Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
entity
-->

# Airbyte Bootstrap Status

## Summary

The bootstrap script has been successfully rewritten to use Airbyte's **public API** (`/api/public/v1/`) instead of the broken internal API (`/api/v1/`).

The main blocker to full automation was Airbyte secret persistence: the Helm chart defaults `SECRET_PERSISTENCE` to `NONE`, which allows Airbyte to generate secret _coordinates_ but not persist the secret _values_. That caused schema discovery workloads to fail with `SecretCoordinateException`.

Setting `SECRET_PERSISTENCE=TESTING_CONFIG_DB_TABLE` (DB-backed secrets) fixes it.

## What Works ✅

- ✅ Public API endpoints (GET /workspaces, GET /sources, GET /destinations)
- ✅ Source creation (Postgres source connector)
- ✅ Destination creation (Postgres destination connector)
- ✅ Connection creation (after enabling secret persistence)
- ✅ Sync jobs run successfully (with a Postgres source reading from a non-Airbyte seed schema)
- ✅ Raw tables populated (`raw.stations`, `raw.water_level_readings`)
- ✅ Airbyte server memory increased to 2Gi (prevents OOM)

## What Fails ❌

- ❌ If Airbyte was installed _before_ secret persistence was enabled, previously-created sources/destinations may still point at secret coordinates whose values were never persisted.
- Symptoms: connection creation fails with HTTP 500 and discover pods show `SecretCoordinateException: That secret was not found in the store!`

## Fix

1. Ensure `SECRET_PERSISTENCE` is set (this repo does it in `k8s/deploy.sh` via `kubectl set env` on the Airbyte deployments).

2. One-time cleanup (only if you created sources/destinations while secret persistence was `NONE`): delete and recreate the affected source/destination so credentials get re-persisted.

After that, the public-API bootstrap can create connections successfully.

## Manual Workaround (UI)

If you prefer, you can still configure sources/destinations/connections via the UI:

### 1. Access Airbyte UI

```bash
kubectl port-forward -n hydro-lineage svc/airbyte-airbyte-webapp-svc 8000:80
# Open http://localhost:8000
```

### 2. Create Source (Postgres - reading from raw tables)

- **Name**: HydroLineage Postgres Source
- **Host**: `airflow-lineage-warehouse-postgresql`
- **Port**: `5432`
- **Database**: `hydro`
- **Schema**: `seed`
- **Username**: `postgres`
- **Password**: Get from secret:
  ```bash
  kubectl get secret airflow-lineage-warehouse-postgresql -n hydro-lineage \
    -o jsonpath='{.data.postgres-password}' | base64 -d
  ```
- **SSL Mode**: Disable
- **Test Connection** → **Set up source**

Why `seed`?

- If you configure a Postgres source to read from `raw`, Airbyte will see `_airbyte_*` columns in the source schema.
- The Postgres destination also adds `_airbyte_*` metadata columns, which can lead to destination failures like:
  - `ERROR: column "_airbyte_raw_id" specified more than once`

### 3. Create Destination (Same Postgres instance, different use case)

- **Name**: HydroLineage Postgres Destination
- **Host**: `airflow-lineage-warehouse-postgresql`
- **Port**: `5432`
- **Database**: `hydro`
- **Schema**: `raw`
- **Username**: `postgres`
- **Password**: (same as above)
- **SSL Mode**: Disable
- **Test Connection** → **Set up destination**

### 4. Create Connections

#### Connection 1: Stations

- **Source**: HydroLineage Postgres Source
- **Destination**: HydroLineage Postgres Destination
- **Name**: UK Flood Stations Sync
- **Replication Frequency**: Manual
- **Streams**: Select `stations` table
- **Sync Mode**: Full Refresh | Overwrite
- **Save connection** → Copy the **Connection ID** from the URL

#### Connection 2: Readings

- **Source**: HydroLineage Postgres Source
- **Destination**: HydroLineage Postgres Destination
- **Name**: UK Flood Readings Sync
- **Replication Frequency**: Manual
- **Streams**: Select `water_level_readings` table
- **Sync Mode**: Full Refresh | Overwrite
- **Save connection** → Copy the **Connection ID** from the URL

### 5. Set Airflow Variables

```bash
# Get Airflow scheduler pod
kubectl get pods -n hydro-lineage | grep scheduler

# Exec into scheduler
kubectl exec -it -n hydro-lineage airflow-lineage-scheduler-xxx -- bash

# Set variables
airflow variables set airbyte_stations_connection_id "<stations-connection-id-from-ui>"
airflow variables set airbyte_readings_connection_id "<readings-connection-id-from-ui>"
```

## Technical Details

### Why Public API?

- Internal API (`/api/v1/source_definitions/list_for_workspace`) returns HTTP 500 NullPointerException
- Public API works for basic operations but has secret storage limitations

### Why Secret Storage Fails?

- The Helm chart defaults `SECRET_PERSISTENCE` to `NONE`.
- Airbyte converts plaintext passwords in `configuration.password` into secret references like `airbyte_workspace_{workspace_id}_secret_{secret_id}_v1`.
- With `SECRET_PERSISTENCE=NONE`, the secret value isn't persisted.
- Discover/check workloads later try to hydrate the secret and fail with `SecretCoordinateException`.

Setting `SECRET_PERSISTENCE=TESTING_CONFIG_DB_TABLE` stores secrets in the config DB and fixes hydration.

### Bootstrap Script Changes

- Converted to public API endpoints
- Removed custom source definition (using standard Postgres connector)
- Changed syncMode from `full_refresh` → `full_refresh_overwrite`
- Added `tunnel_method` config
- Fixed secret key: `password` → `postgres-password`
- Updated service names for K8s DNS

## Files Modified

- `k8s/airbyte_bootstrap.py` - Rewritten for public API
- `k8s/deploy.sh` - Updated API base URL and secret handling
- `k8s/airbyte-values.yaml` - Increased server memory to 2Gi; set `SECRET_PERSISTENCE`

## Future Improvements

- Upgrade to newer Airbyte version with better public API secret handling
- OR use Terraform/Helm provider for Airbyte resource management
- OR implement Airbyte's secret store integration directly

## Raw Tables Schema

The current bootstrap approach expects a **seed schema** that contains domain columns only (no `_airbyte_*`):

```sql
CREATE SCHEMA IF NOT EXISTS seed;

CREATE TABLE IF NOT EXISTS seed.stations (
  notation text PRIMARY KEY,
  label text NOT NULL,
  lat double precision NOT NULL,
  long double precision NOT NULL,
  "riverName" text,
  "stationReference" text,
  town text,
  status text,
  easting integer,
  northing integer,
  "catchmentName" text,
  "dateOpened" date,
  "wiskiID" text,
  "RLOIid" text,
  _id text
);

CREATE TABLE IF NOT EXISTS seed.water_level_readings (
  reading_id text PRIMARY KEY,
  measure_id text NOT NULL,
  reading_datetime timestamptz NOT NULL,
  station_id text NOT NULL,
  value double precision NOT NULL
);
```

Airbyte then writes into `raw.*` (configured on the destination) and adds the `_airbyte_*` metadata columns that dbt expects.
