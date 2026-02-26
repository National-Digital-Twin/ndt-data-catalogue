# SPDX-License-Identifier: Apache-2.0
#
# © Crown Copyright 2025. This work has been developed by the National Digital Twin
# Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
# entity

"""
Comprehensive connectivity test DAG for HydroLineage platform
Tests connections to: PostgreSQL, dbt, DataHub, Airbyte, Redis healthcheck_hydro_dag.py
"""

from datetime import datetime, timedelta
from airflow.models.dag import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
import os

default_args = {
    'owner': 'hydro-team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

def print_hello():
    """Simple Python function"""
    print("Hello from HydroLineage!")
    print("Airflow is working correctly!")
    return "Success"

def print_context(**context):
    """Print Airflow context"""
    print("Airflow Context:")
    print(f"  Available keys: {list(context.keys())}")
    print(f"  DAG run: {context.get('dag_run', 'N/A')}")
    print(f"  Task instance: {context.get('task_instance', 'N/A')}")
    print(f"  Logical date: {context.get('logical_date', context.get('data_interval_start', 'N/A'))}")

def test_postgres_connection():
    """Test PostgreSQL warehouse connection"""
    import psycopg2
    host = os.getenv('POSTGRES_HOST', 'airflow-lineage-warehouse-postgresql')
    port = os.getenv('POSTGRES_PORT', '5432')
    database = os.getenv('POSTGRES_DB', 'hydro')
    user = os.getenv('DBT_USER', 'postgres')
    password = os.getenv('POSTGRES_PASSWORD', 'hydro_secure_password_2024')
    
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            connect_timeout=5
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ PostgreSQL connection successful!")
        print(f"   Host: {host}:{port}")
        print(f"   Database: {database}")
        print(f"   Version: {version[0][:50]}...")
        cursor.close()
        conn.close()
        return "PostgreSQL: OK"
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        raise

def test_datahub_connection():
    """Test DataHub GMS API connection"""
    import requests
    
    # Try both internal and external DataHub URLs
    urls = [
        os.getenv('AIRFLOW_CONN_DATAHUB_REST', 'http://datahub-datahub-gms.datahub.svc.cluster.local:8080'),
        'http://datahub-gms:8080',
        'http://datahub-datahub-gms:8080'
    ]
    
    for url in urls:
        # Extract just the base URL
        base_url = url.replace('http://:@', 'http://').split('@')[-1]
        health_url = f"{base_url}/health"
        
        try:
            response = requests.get(health_url, timeout=5)
            if response.status_code == 200:
                print(f"✅ DataHub GMS connection successful!")
                print(f"   URL: {base_url}")
                print(f"   Status: {response.status_code}")
                return f"DataHub: OK ({base_url})"
        except Exception as e:
            print(f"⚠️  DataHub attempt failed for {base_url}: {e}")
            continue
    
    print("❌ DataHub connection failed on all URLs")
    print("   This is expected if DataHub is not deployed")
    return "DataHub: Not Available (optional)"

def test_airbyte_connection():
    """Test Airbyte API connection and pipeline-required connection IDs."""
    import requests
    from airflow.hooks.base import BaseHook
    from airflow.models import Variable
    
    def _validate_pipeline_connections(base: str, auth):
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
                "Airbyte API is reachable, but the pipeline is not configured. Missing Airflow Variables: "
                + ", ".join(missing)
            )

        for label, connection_id in [("stations", stations_id), ("readings", readings_id)]:
            resp = requests.post(
                f"{base}/api/v1/connections/get",
                json={"connectionId": connection_id},
                timeout=10,
                auth=auth,
            )
            if resp.status_code == 404:
                raise ValueError(
                    f"Airbyte connection ID for {label} not found: {connection_id}. "
                    "Update the corresponding Airflow Variable with the correct UUID from Airbyte UI."
                )
            resp.raise_for_status()

    # Prefer testing via the same Airflow connection used by the pipeline.
    # This catches misconfigurations in AIRFLOW_CONN_AIRBYTE_DEFAULT.
    try:
        conn = BaseHook.get_connection('airbyte_default')
        scheme = conn.schema or 'http'
        host = conn.host
        port = conn.port
        if host:
            base = f"{scheme}://{host}" + (f":{port}" if port else "")
            auth = (conn.login, conn.password) if conn.login or conn.password else None
            response = requests.get(f"{base}/api/v1/health", timeout=5, auth=auth)
            if response.status_code == 200:
                _validate_pipeline_connections(base, auth)  # Let ValueError propagate
                print(f"✅ Airbyte API connection successful!")
                print(f"   URL: {base}")
                print(f"   Status: {response.status_code}")
                data = response.json()
                print(f"   Available: {data.get('available', 'unknown')}")
                return f"Airbyte: OK ({base})"
    except ValueError:
        # Re-raise ValueError for missing/invalid Airbyte connection IDs
        raise
    except Exception as e:
        print(f"⚠️  Airbyte via Airflow connection failed: {e}")

    # Fallback: try common in-cluster service names.
    urls = [
        'http://airbyte-airbyte-server-svc:8001',
        'http://airbyte-server:8001'
    ]

    for url in urls:
        try:
            health_url = f"{url}/api/v1/health"
            response = requests.get(health_url, timeout=5)
            if response.status_code == 200:
                _validate_pipeline_connections(url, auth=None)  # Let ValueError propagate
                print(f"✅ Airbyte API connection successful!")
                print(f"   URL: {url}")
                print(f"   Status: {response.status_code}")
                data = response.json()
                print(f"   Available: {data.get('available', 'unknown')}")
                return f"Airbyte: OK ({url})"
        except ValueError:
            # Re-raise ValueError for missing/invalid Airbyte connection IDs
            raise
        except Exception as e:
            print(f"⚠️  Airbyte attempt failed for {url}: {e}")
            continue
    
    print("❌ Airbyte connection failed on all URLs")
    print("   This is expected if Airbyte is not deployed")
    return "Airbyte: Not Available (optional)"

def test_datahub_plugin():
    """Test DataHub Airflow plugin installation and configuration"""
    import sys
    from airflow.configuration import conf
    
    # Add extra_python_packages to path if not already there
    extra_packages_path = '/opt/airflow/extra_python_packages'
    if extra_packages_path not in sys.path:
        sys.path.insert(0, extra_packages_path)
    
    print("🔍 Checking DataHub Airflow Plugin...")
    
    # Check 1: Plugin is importable
    try:
        import datahub_airflow_plugin
        version = getattr(datahub_airflow_plugin, '__version__', 'unknown')
        print(f"✅ DataHub plugin installed: v{version}")
    except ImportError as e:
        print(f"❌ DataHub plugin not installed: {e}")
        raise
    
    # Check 2: Lineage backend is configured
    try:
        lineage_backend = conf.get('lineage', 'backend', fallback=None)
        if lineage_backend:
            print(f"✅ Lineage backend configured: {lineage_backend}")
            if 'datahub' not in lineage_backend.lower():
                print(f"⚠️  Warning: Lineage backend doesn't appear to be DataHub")
        else:
            print("❌ No lineage backend configured in [lineage] section")
            raise ValueError("lineage.backend not set in airflow.cfg")
    except Exception as e:
        print(f"❌ Failed to check lineage backend: {e}")
        raise
    
    # Check 3: DataHub config section exists
    try:
        datahub_enabled = conf.getboolean('datahub', 'enabled', fallback=False)
        datahub_conn_id = conf.get('datahub', 'conn_id', fallback=None)
        patch_sql = conf.getboolean('datahub', 'patch_sql_parser', fallback=False)
        
        print(f"✅ DataHub config section:")
        print(f"   enabled: {datahub_enabled}")
        print(f"   conn_id: {datahub_conn_id}")
        print(f"   patch_sql_parser: {patch_sql}")
        
        if not datahub_enabled:
            raise ValueError("datahub.enabled is False")
        if not datahub_conn_id:
            raise ValueError("datahub.conn_id not set")
    except Exception as e:
        print(f"❌ DataHub configuration error: {e}")
        raise
    
    # Check 4: DataHub connection exists
    try:
        from airflow.hooks.base import BaseHook
        conn = BaseHook.get_connection(datahub_conn_id)
        print(f"✅ DataHub connection '{datahub_conn_id}' exists:")
        print(f"   host: {conn.host}")
        print(f"   port: {conn.port}")
    except Exception as e:
        print(f"❌ DataHub connection error: {e}")
        raise
    
    print("✅ DataHub plugin verification complete!")
    return "DataHub Plugin: OK"

def print_environment():
    """Print relevant environment variables"""
    print("🔍 Environment Configuration:")
    print(f"   POSTGRES_HOST: {os.getenv('POSTGRES_HOST', 'not set')}")
    print(f"   POSTGRES_DB: {os.getenv('POSTGRES_DB', 'not set')}")
    print(f"   AIRFLOW_CONN_DATAHUB_REST: {os.getenv('AIRFLOW_CONN_DATAHUB_REST', 'not set')}")
    print(f"   Kubernetes namespace: {os.getenv('AIRFLOW__CORE__NAMESPACE', 'not set')}")
    return "Environment: OK"

with DAG(
    'healthcheck_hydro',
    default_args=default_args,
    description='Comprehensive connectivity test for HydroLineage platform',
    schedule=None,  # Manual trigger only
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['test', 'connectivity', 'health-check'],
) as dag:

    # Task 1: Print using bash
    hello_bash = BashOperator(
        task_id='hello_bash',
        bash_command='echo "🌊 Hello from HydroLineage Platform!"',
    )

    # Task 2: Print using Python
    hello_python = PythonOperator(
        task_id='hello_python',
        python_callable=print_hello,
    )

    # Task 3: Print context
    print_airflow_context = PythonOperator(
        task_id='print_context',
        python_callable=print_context,
    )

    # Task 4: Print environment
    print_env = PythonOperator(
        task_id='print_environment',
        python_callable=print_environment,
    )

    # Task 5: Check dbt is available
    check_dbt = BashOperator(
        task_id='check_dbt',
        bash_command='export PATH=$PATH:/home/airflow/.local/bin && dbt --version || echo "⚠️  dbt not found in PATH. Install via init container or pip."',
        trigger_rule='all_done',  # Don't fail if dbt not installed
    )

    # Task 6: Check PostgreSQL CLI
    check_postgres_cli = BashOperator(
        task_id='check_postgres_cli',
        bash_command='psql --version || echo "⚠️  psql not found. Install postgresql-client if needed."',
        trigger_rule='all_done',  # Don't fail if psql not installed
    )

    # Task 7: Test PostgreSQL warehouse connection
    test_postgres = PythonOperator(
        task_id='test_postgres_connection',
        python_callable=test_postgres_connection,
    )

    # Task 8: Test DataHub plugin installation
    test_datahub_plugin_task = PythonOperator(
        task_id='test_datahub_plugin',
        python_callable=test_datahub_plugin,
        trigger_rule='all_done',  # Run even if upstream fails
    )
    
    # Task 9: Test DataHub GMS API connection (optional)
    test_datahub = PythonOperator(
        task_id='test_datahub_connection',
        python_callable=test_datahub_connection,
        trigger_rule='all_done',  # Run even if upstream fails
    )

    # Task 10: Test Airbyte connection (optional)
    test_airbyte = PythonOperator(
        task_id='test_airbyte_connection',
        python_callable=test_airbyte_connection,
        trigger_rule='all_done',  # Run even if upstream fails
    )

    # Task 11: Final summary
    summary = BashOperator(
        task_id='connectivity_summary',
        bash_command='echo "✅ Platform connectivity check complete! Check logs above for details."',
        trigger_rule='all_done',
    )

    # Define dependencies - fan-out pattern for parallel testing
    hello_bash >> hello_python >> print_airflow_context >> print_env
    
    # Core service checks (PostgreSQL must succeed, others can fail gracefully)
    print_env >> [check_dbt, check_postgres_cli, test_postgres]
    
    # Optional service checks (can fail)
    print_env >> [test_datahub_plugin_task, test_airbyte]
    
    # DataHub plugin check should run before API check
    test_datahub_plugin_task >> test_datahub
    
    # PostgreSQL is critical, others converge to summary
    test_postgres >> summary
    [check_dbt, check_postgres_cli, test_datahub, test_airbyte] >> summary
