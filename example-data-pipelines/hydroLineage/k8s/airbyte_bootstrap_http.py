#!/usr/bin/env python
# SPDX-License-Identifier: Apache-2.0
#
# © Crown Copyright 2025. This work has been developed by the National Digital Twin
# Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
# entity

"""
Airbyte HTTP API Source Bootstrap for UK Flood Monitoring API

This uses a Python script to fetch data from the UK Flood Monitoring API,
then seeds it into Postgres. Airbyte then syncs Postgres->Postgres for lineage tracking.

This is a common pattern for APIs without native Airbyte connectors:
API -> Python extraction -> Staging DB -> Airbyte (for lineage) -> Warehouse
"""
import requests
import psycopg2
from datetime import datetime

API_BASE = "https://environment.data.gov.uk/flood-monitoring"

def fetch_stations(limit=100):
    """Fetch stations from UK Flood API"""
    resp = requests.get(f"{API_BASE}/id/stations", params={"_limit": limit}, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data.get("items", [])

def fetch_readings(limit=1000):
    """Fetch water level readings from UK Flood API"""
    resp = requests.get(
        f"{API_BASE}/data/readings",
        params={"parameter": "level", "_limit": limit},
        timeout=30
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("items", [])

def load_to_postgres(host, port, db, user, password):
    """Load API data into seed schema for Airbyte to sync"""
    conn = psycopg2.connect(
        host=host, port=port, database=db, user=user, password=password
    )
    cur = conn.cursor()
    
    # Fetch from API
    print("Fetching stations from UK Flood API...")
    stations = fetch_stations()
    print(f"Fetched {len(stations)} stations")
    
    print("Fetching readings from UK Flood API...")
    readings = fetch_readings()
    print(f"Fetched {len(readings)} readings")
    
    # Truncate and reload seed tables
    cur.execute("TRUNCATE TABLE seed.stations, seed.water_level_readings CASCADE")
    
    # Insert stations
    for station in stations:
        cur.execute("""
            INSERT INTO seed.stations (
                notation, label, lat, long, "riverName", "stationReference",
                town, status, easting, northing, "catchmentName", 
                "dateOpened", "wiskiID", "RLOIid", _id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (notation) DO NOTHING
        """, (
            station.get("notation"),
            station.get("label"),
            station.get("lat"),
            station.get("long"),
            station.get("riverName"),
            station.get("stationReference"),
            station.get("town"),
            station.get("status"),
            station.get("easting"),
            station.get("northing"),
            station.get("catchmentName"),
            station.get("dateOpened"),
            station.get("wiskiID"),
            station.get("RLOIid"),
            station.get("@id")
        ))
    
    # Insert readings
    for reading in readings:
        measure = reading.get("measure", "")
        cur.execute("""
            INSERT INTO seed.water_level_readings (
                reading_id, measure_id, reading_datetime, station_id, value
            ) VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (reading_id) DO NOTHING
        """, (
            f"{measure}_{reading.get('dateTime')}",
            measure,
            reading.get("dateTime"),
            measure.split("/")[-1] if "/" in measure else "",
            reading.get("value")
        ))
    
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Loaded {len(stations)} stations and {len(readings)} readings to seed schema")

if __name__ == "__main__":
    import os
    load_to_postgres(
        host=os.environ.get("PGHOST", "localhost"),
        port=int(os.environ.get("PGPORT", "5432")),
        db=os.environ.get("PGDATABASE", "hydro"),
        user=os.environ.get("PGUSER", "postgres"),
        password=os.environ["PGPASSWORD"]
    )
