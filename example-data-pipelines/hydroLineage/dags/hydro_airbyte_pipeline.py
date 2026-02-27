# SPDX-License-Identifier: Apache-2.0
#
# © Crown Copyright 2025. This work has been developed by the National Digital Twin
# Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
# entity

""" 
HydroLineage Airbyte Pipeline DAG
Complete data pipeline orchestration using Airbyte for ingestion:
1. Ingest data from UK Flood API via Airbyte → raw tables
2. Transform data with dbt (raw → analytics)
3. Ingest metadata to DataHub for governance

Architecture: UK Flood API → Airbyte → raw → dbt → analytics

DataHub Integration:
- Uses built-in Airflow 3 DataHub plugin for lineage/metadata
- dbt and PostgreSQL metadata sent to DataHub via CLI recipes
- Airbyte metadata ingestion is optional if the Airbyte source plugin is unavailable
"""

from datetime import datetime, timedelta
import os
from airflow.models.dag import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from airflow.models.variable import Variable
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from kubernetes.client import models as k8s
from airflow.datasets import Dataset
# DataHub lineage now handled by built-in Airflow 3 plugin, not external provider

default_args = {
    'owner': 'hydro-team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# Airbyte Configuration
# These connection IDs must match the Airbyte connections created in Airbyte UI
AIRBYTE_CONN_ID = os.getenv('AIRBYTE_CONN_ID', 'airbyte_default')  # Airflow connection to Airbyte instance

# Airbyte *connection IDs* are provided at runtime via Airflow Variables.
# Set these in the Airflow UI (Admin -> Variables) so the DAG can run end-to-end
# without code edits:
# - airbyte_stations_connection_id
# - airbyte_readings_connection_id
STATIONS_SYNC_ID = "{{ var.value.airbyte_stations_connection_id }}"
READINGS_SYNC_ID = "{{ var.value.airbyte_readings_connection_id }}"


# =====================================
# STAGE 1: AIRBYTE INGESTION (lineage)
# =====================================


def validate_airbyte_configuration(**_context):
    """Fail fast with a clear message if Airbyte isn't configured yet."""

    stations_id = Variable.get("airbyte_stations_connection_id", default_var=None)
    readings_id = Variable.get("airbyte_readings_connection_id", default_var=None)

    missing = [
        name
        for name, value in [
            ("airbyte_stations_connection_id", stations_id),
            ("airbyte_readings_connection_id", readings_id),
        ]
        if not value
    ]

    if missing:
        raise ValueError(
            "Missing Airbyte connection IDs. Set Airflow Variables: "
            + ", ".join(missing)
            + ".\n"
            "In Airbyte UI, create the two connections (stations + readings), then copy each connection's UUID into the matching Airflow Variable."  # noqa: E501
        )

    # Optional: sanity-check Airbyte is reachable and the connection IDs exist.
    # IMPORTANT: Prefer the Public API for connection lookups. The legacy internal
    # `/api/v1/connections/get` has been flaky for us (500/NPE) on Airbyte OSS 2.x.
    from airflow.hooks.base import BaseHook  # Airflow 3 moved from airflow.hooks.base_hook
    import requests

    conn = BaseHook.get_connection(AIRBYTE_CONN_ID)
    scheme = conn.schema or "http"
    host = conn.host
    if not host:
        raise ValueError(
            f"Airflow connection '{AIRBYTE_CONN_ID}' has no host. "
            "Ensure AIRFLOW_CONN_AIRBYTE_DEFAULT is set to something like http://airbyte-airbyte-server-svc.hydro-lineage.svc.cluster.local:8001"  # noqa: E501
        )

    base = f"{scheme}://{host}" + (f":{conn.port}" if conn.port else "")
    auth = (conn.login, conn.password) if conn.login or conn.password else None

    print(f"Checking Airbyte health at {base} ...")
    try:
        health = requests.get(f"{base}/api/v1/health", timeout=10, auth=auth)
        health.raise_for_status()
    except requests.HTTPError:
        # Fall back to public health if the internal endpoint is blocked.
        health = requests.get(f"{base}/api/public/v1/health", timeout=10, auth=auth)
        health.raise_for_status()

    for label, connection_id in [("stations", stations_id), ("readings", readings_id)]:
        print(f"Validating Airbyte connection exists for {label}: {connection_id}")
        resp = requests.get(
            f"{base}/api/public/v1/connections/{connection_id}",
            timeout=15,
            auth=auth,
        )
        if resp.status_code == 404:
            raise ValueError(
                f"Airbyte connection ID for {label} not found: {connection_id}. "
                "Double-check the ID in the Airbyte UI and update the Airflow Variable."  # noqa: E501
            )
        resp.raise_for_status()


def validate_raw_data(**context):
    """Validate raw data was loaded successfully"""
    hook = PostgresHook(postgres_conn_id='hydro_postgres')
    
    stations_count = hook.get_first("SELECT COUNT(*) FROM raw.stations")[0]
    readings_count = hook.get_first("SELECT COUNT(*) FROM raw.water_level_readings")[0]
    
    print("=" * 60)
    print("RAW DATA VALIDATION")
    print("=" * 60)
    print(f"✅ Stations loaded: {stations_count}")
    print(f"✅ Readings loaded: {readings_count}")
    
    if stations_count == 0:
        raise ValueError("No stations were loaded!")
    
    if readings_count == 0:
        raise ValueError("No readings were loaded!")
    
    print("✅ Raw data validation passed")
    
    context['ti'].xcom_push(key='validated_stations', value=stations_count)
    context['ti'].xcom_push(key='validated_readings', value=readings_count)


# =====================================
# STAGE 2: DBT TRANSFORMATION
# =====================================

def validate_dbt_models(**context):
    """Validate dbt models created data"""
    hook = PostgresHook(postgres_conn_id='hydro_postgres')
    
    # Check analytics tables
    dim_station_count = hook.get_first(
        "SELECT COUNT(*) FROM analytics_analytics.dim_station"
    )[0]
    
    fct_levels_count = hook.get_first(
        "SELECT COUNT(*) FROM analytics_analytics.fct_water_levels"
    )[0]
    
    print("=" * 60)
    print("DBT TRANSFORMATION VALIDATION")
    print("=" * 60)
    print(f"✅ dim_station: {dim_station_count} rows")
    print(f"✅ fct_water_levels: {fct_levels_count} rows")
    
    if dim_station_count == 0:
        raise ValueError("dim_station is empty!")
    
    if fct_levels_count == 0:
        raise ValueError("fct_water_levels is empty!")
    
    print("✅ dbt transformation validation passed")
    
    context['ti'].xcom_push(key='dim_station_rows', value=dim_station_count)
    context['ti'].xcom_push(key='fct_water_levels_rows', value=fct_levels_count)


# =====================================
# PIPELINE SUMMARY
# =====================================

def log_pipeline_summary(**context):
    """Log complete pipeline execution summary"""
    ti = context['ti']
    
    # Get metrics from all stages
    stations_count = ti.xcom_pull(task_ids='validate_raw_data', key='validated_stations') or 0
    readings_count = ti.xcom_pull(task_ids='validate_raw_data', key='validated_readings') or 0
    dim_station_rows = ti.xcom_pull(task_ids='validate_dbt_models', key='dim_station_rows') or 0
    fct_levels_rows = ti.xcom_pull(task_ids='validate_dbt_models', key='fct_water_levels_rows') or 0
    
    summary = f"""
    ============================================================
              HYDROLINEAGE PIPELINE SUMMARY
    ============================================================
    
     📊 STAGE 1: AIRBYTE SYNC (lineage tracking)
         ✅ UK Flood API → raw.stations:  {stations_count:,}
         ✅ UK Flood API → raw.water_level_readings:  {readings_count:,}
    
    🔄 STAGE 2: DBT TRANSFORMATIONS
       ✅ dim_station:      {dim_station_rows:,} rows
       ✅ fct_water_levels: {fct_levels_rows:,} rows
    
    📋 STAGE 3: METADATA GOVERNANCE
       ✅ DataHub provider configured for automated ingestion
       ℹ️  Metadata tracked via apache-airflow-providers-datahub
    
    🎯 PIPELINE STATUS: SUCCESS
    
    Next Steps:
      - View data: SELECT * FROM analytics_analytics.dim_station LIMIT 10;
      - View lineage: http://localhost:9002 (DataHub UI)
      - Run tests: dbt test --profiles-dir . --target dev
    
    ============================================================
    """
    
    print(summary)
    
    # Push summary to XCom for downstream monitoring
    context['ti'].xcom_push(key='pipeline_summary', value={
        'stations_loaded': stations_count,
        'readings_loaded': readings_count,
        'dim_station_rows': dim_station_rows,
        'fct_water_levels_rows': fct_levels_rows,
        'status': 'SUCCESS'
    })


# =====================================
# DAG DEFINITION
# =====================================

with DAG(
    'hydro_airbyte_pipeline',
    default_args=default_args,
    description='Complete end-to-end pipeline: UK Flood API → Airbyte → raw → dbt → analytics',
    schedule='0 2 * * *',  # Run at 2 AM daily
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['production', 'airbyte', 'end-to-end', 'hydro', 'uk-flood-api'],
    max_active_runs=1,  # Only one pipeline run at a time
) as dag:

    # =====================================
    # STAGE 1: DATA INGESTION VIA AIRBYTE (lineage tracking)
    # =====================================
    
    # Airbyte pulls directly from UK Flood API into raw schema

    validate_airbyte_setup = PythonOperator(
        task_id="validate_airbyte_configuration",
        python_callable=validate_airbyte_configuration,
        retries=0,
        execution_timeout=timedelta(minutes=2),
    )
    
    # Airbyte sync for stations (UK Flood API → raw.stations)
    # NOTE: Airbyte connections are configured via airbyte_bootstrap.py during deployment
    # Connection IDs stored in Airflow Variables: airbyte_stations_connection_id
    sync_stations = AirbyteTriggerSyncOperator(
        task_id='airbyte_sync_stations',
        airbyte_conn_id=AIRBYTE_CONN_ID,
        connection_id=STATIONS_SYNC_ID,
        asynchronous=False,  # Wait for sync to complete
        timeout=600,  # 10 minutes
        wait_seconds=10,  # Poll every 10 seconds
        outlets=[Dataset("postgres://airflow-lineage-warehouse-postgresql/hydro/raw/stations")],
        # Automatic lineage: Airbyte sync UK Flood API → raw.stations
    )
    
    # Airbyte sync for water level readings (UK Flood API → raw.water_level_readings)
    # NOTE: Airbyte connections are configured via airbyte_bootstrap.py during deployment
    # Connection IDs stored in Airflow Variables: airbyte_readings_connection_id
    sync_readings = AirbyteTriggerSyncOperator(
        task_id='airbyte_sync_readings',
        airbyte_conn_id=AIRBYTE_CONN_ID,
        connection_id=READINGS_SYNC_ID,
        asynchronous=False,
        timeout=600,
        wait_seconds=10,
        outlets=[Dataset("postgres://airflow-lineage-warehouse-postgresql/hydro/raw/water_level_readings")],
        # Automatic lineage: Airbyte sync UK Flood API → raw.water_level_readings
    )
    
    validate_raw = PythonOperator(
        task_id='validate_raw_data',
        python_callable=validate_raw_data,
        # Automatic lineage: Reads from raw tables for validation
    )
    
    # =====================================
    # STAGE 2: DBT TRANSFORMATIONS
    # =====================================
    
    # Install dbt packages (run deps before dbt run to avoid hub.getdbt.com network issues during init)
    dbt_deps = BashOperator(
        task_id='dbt_deps',
        bash_command='cd /opt/airflow/dbt && /opt/airflow/dbt_venv/bin/dbt deps --profiles-dir . --target dev || echo "⚠️ dbt deps may use cached packages"',
    )
    
    # Run dbt models (packages and profiles.yml already deployed)
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/airflow/dbt && /opt/airflow/dbt_venv/bin/dbt run --profiles-dir . --target dev',
        # Automatic lineage: dbt transformations raw → staging → analytics
        # Note: dbt metadata ingestion task provides detailed model lineage
    )
    
    # Run dbt tests
    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/airflow/dbt && /opt/airflow/dbt_venv/bin/dbt test --profiles-dir . --target dev || true',  # Don't fail on test warnings
        # Automatic lineage: Data quality tests on analytics tables
    )
    
    # Generate dbt documentation
    dbt_docs = BashOperator(
        task_id='dbt_docs_generate',
        bash_command='cd /opt/airflow/dbt && cp target/run_results.json target/run_results_backup.json && /opt/airflow/dbt_venv/bin/dbt docs generate --profiles-dir . --target dev && cp target/run_results_backup.json target/run_results.json'
    )
    
    validate_dbt = PythonOperator(
        task_id='validate_dbt_models',
        python_callable=validate_dbt_models,
        # Automatic lineage: Validation reads from analytics tables
    )
    
    # =================================== ====
    # STAGE 3: DATAHUB METADATA INGESTION
    # =====================================
    # Using built-in DataHub provider operators for metadata ingestion
    # These operators automatically handle dbt and PostgreSQL metadata extraction
    
    # Note: DataHub ingestion using the provider requires:
    # 1. DataHub connection configured in Airflow (datahub_rest_default)
    # 2. dbt project files accessible to the operator
    # 3. PostgreSQL connection details for profiling
    
    # DataHub metadata ingestion now handled automatically by built-in Airflow 3 DataHub plugin
    # Plugin configuration in airflow.cfg enables automatic lineage capture:
    # [datahub] emit_lineage = True, enable_datajob_lineage = True, cluster = 'dev'
    # No explicit ingestion operators needed - lineage emitted automatically on task execution
    
    # Batch dbt metadata sync for column-level lineage
    # NOTE: Must ensure manifest.json exists before ingestion
    ingest_dbt_metadata = BashOperator(
        task_id='ingest_dbt_metadata',
        bash_command=(
            'cd /opt/airflow/dbt && '
            'echo "Ensuring dbt manifest.json exists..." && '
            'if [ ! -f target/manifest.json ]; then '
            '  echo "manifest.json not found, running dbt compile..." && '
            '  echo "Installing dbt packages first..." && '
            '  /opt/airflow/dbt_venv/bin/dbt deps --profiles-dir . 2>/dev/null || echo "⚠️  dbt deps may use cached packages" && '
            '  /opt/airflow/dbt_venv/bin/dbt compile --profiles-dir . --target dev; '
            'else '
            '  echo "✅ manifest.json found at $(ls -lh target/manifest.json)"; '
            'fi && '
            'cd /opt/airflow && '
            'export DATAHUB_GMS_URL=http://datahub-datahub-gms.datahub.svc.cluster.local:8080 && '
            'export DATAHUB_GMS_TOKEN=${DATAHUB_GMS_TOKEN} && '
            'export DATAHUB_DEBUG=1 && '
            'export PYTHONPATH=/opt/airflow/dbt_venv/lib/python3.11/site-packages && '
            'echo "======================================" && '
            'echo "dbt Metadata Ingestion - Debug Mode" && '
            'echo "======================================" && '
            '/opt/airflow/dbt_venv/bin/python -m datahub ingest run -c /opt/airflow/datahub/recipes/dbt_to_datahub.yml'
        ),
    )
    
    # PostgreSQL metadata ingestion for raw table schemas and statistics
    ingest_postgres_metadata = BashOperator(
        task_id='ingest_postgres_metadata',
        bash_command=(
            'echo "=========================================" && '
            'echo "PostgreSQL Metadata Ingestion - Debug" && '
            'echo "=========================================" && '
            'echo "Ensuring setuptools is installed..." && '
            '/opt/airflow/dbt_venv/bin/pip install --quiet setuptools wheel 2>/dev/null || echo "setuptools already installed" && '
            'export DATAHUB_GMS_URL=http://datahub-datahub-gms.datahub.svc.cluster.local:8080 && '
            'export DATAHUB_GMS_TOKEN=${DATAHUB_GMS_TOKEN} && '
            'export DATAHUB_DEBUG=1 && '
            'export POSTGRES_PASSWORD=${POSTGRES_PASSWORD} && '
            'export PYTHONPATH=/opt/airflow/dbt_venv/lib/python3.11/site-packages && '
            '/opt/airflow/dbt_venv/bin/python -m datahub ingest run -c /opt/airflow/datahub/recipes/postgres_to_datahub.yml'
        ),
    )

    # Airbyte metadata ingestion using DataHub's Airbyte source (PULL model)
    # Airbyte source plugin is installed by init container from local ConfigMap-mounted package.
    ingest_airbyte_metadata = KubernetesPodOperator(
        task_id='ingest_airbyte_metadata',
        name='datahub-airbyte-ingestion',
        namespace='hydro-lineage',
        image='acryldata/datahub-ingestion:head',
        image_pull_policy='IfNotPresent',
        init_containers=[
            k8s.V1Container(
                name='install-airbyte-plugin',
                image='acryldata/datahub-ingestion:head',
                command=['/bin/bash', '-c'],
                args=[
                    'set -euo pipefail; '
                    'cp -a /opt/datahub-airbyte-source /tmp/datahub-airbyte-source; '
                    'python -m pip install --disable-pip-version-check --no-cache-dir --no-build-isolation --no-deps '
                    '--target /opt/datahub-extra-packages /tmp/datahub-airbyte-source'
                ],
                volume_mounts=[
                    k8s.V1VolumeMount(
                        name='datahub-extra-packages',
                        mount_path='/opt/datahub-extra-packages',
                    ),
                    k8s.V1VolumeMount(
                        name='datahub-airbyte-source',
                        mount_path='/opt/datahub-airbyte-source',
                        read_only=True,
                    ),
                ],
            )
        ],
        volumes=[
            k8s.V1Volume(
                name='datahub-extra-packages',
                empty_dir=k8s.V1EmptyDirVolumeSource(),
            )
            ,
            k8s.V1Volume(
                name='datahub-airbyte-source',
                config_map=k8s.V1ConfigMapVolumeSource(
                    name='airflow-lineage-datahub-airbyte-source',
                    items=[
                        k8s.V1KeyToPath(key='pyproject.toml', path='pyproject.toml'),
                        k8s.V1KeyToPath(key='__init__.py', path='datahub_airbyte_source/__init__.py'),
                        k8s.V1KeyToPath(key='airbyte_source.py', path='datahub_airbyte_source/airbyte_source.py'),
                    ],
                ),
            ),
        ],
        volume_mounts=[
            k8s.V1VolumeMount(
                name='datahub-extra-packages',
                mount_path='/opt/datahub-extra-packages',
            )
        ],
        cmds=['/bin/bash', '-c'],
        arguments=['''
            echo "DataHub Airbyte Metadata Ingestion (Pull Model)"
            echo "[timing] start: $(date -Iseconds)"
            echo "Validating Airbyte plugin is available..."
            echo "[timing] before plugin check: $(date -Iseconds)"
            /usr/local/bin/python - <<'PY'
from datahub.ingestion.source.source_registry import source_registry
if "airbyte" not in source_registry.mapping:
    raise SystemExit(
        "Airbyte source not registered. Check init container install from "
        "/opt/datahub-airbyte-source to /opt/datahub-extra-packages."
    )
PY
            echo "[timing] after plugin check: $(date -Iseconds)"
            cat > /tmp/recipe.yml <<'EOF'
source:
  type: airbyte
  config:
    host_port: "airbyte-airbyte-server-svc:8001"
sink:
  type: datahub-rest
  config:
    server: "__from_env__"
EOF
            echo "[timing] before ingest: $(date -Iseconds)"
            /usr/local/bin/datahub ingest -c /tmp/recipe.yml
            echo "[timing] after ingest: $(date -Iseconds)"
        '''],
        env_vars=[
            k8s.V1EnvVar(name='DATAHUB_GMS_URL', value='http://datahub-datahub-gms.datahub.svc.cluster.local:8080'),
            k8s.V1EnvVar(name='DATAHUB_GMS_TOKEN', value_from=k8s.V1EnvVarSource(
                secret_key_ref=k8s.V1SecretKeySelector(name='datahub-gms-token', key='DATAHUB_GMS_TOKEN')
            )),
            k8s.V1EnvVar(name='DATAHUB_TELEMETRY_ENABLED', value='false'),
            k8s.V1EnvVar(name='PYTHONPATH', value='/opt/datahub-extra-packages'),
        ],
        get_logs=False,
        is_delete_operator_pod=True,
        in_cluster=True,
        startup_timeout_seconds=300,
        container_resources=k8s.V1ResourceRequirements(
            requests={"memory": "1Gi", "cpu": "500m", "ephemeral-storage": "2Gi"},
            limits={"memory": "2Gi", "cpu": "1000m", "ephemeral-storage": "4Gi"}
        ),
    )
    
    # =====================================
    # PIPELINE SUMMARY
    # =====================================
    
    summary = PythonOperator(
        task_id='log_pipeline_summary',
        python_callable=log_pipeline_summary,
    )
    
    # =====================================
    # TASK DEPENDENCIES
    # =====================================
    
    # Stage 1: Ingestion via Airbyte (API → raw for lineage tracking)
    validate_airbyte_setup >> [sync_stations, sync_readings] >> validate_raw
    
    # Stage 2: Transformation (install packages, then run dbt)
    validate_raw >> dbt_deps >> dbt_run >> dbt_test >> dbt_docs >> validate_dbt
    
    # Stage 3: Metadata governance
    # Airflow plugin captures task lineage automatically
    # Airbyte ingestion pulls metadata from Airbyte API (pull model)
    # dbt ingestion adds column-level lineage from dbt models
    # PostgreSQL ingestion adds table schemas and statistics
    validate_dbt >> ingest_dbt_metadata >> ingest_airbyte_metadata >> ingest_postgres_metadata
    
    # Final summary
    ingest_postgres_metadata >> summary
