#!/usr/bin/env python
# SPDX-License-Identifier: Apache-2.0
#
# © Crown Copyright 2025. This work has been developed by the National Digital Twin
# Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
# entity

"""Airbyte bootstrap for HydroLineage (run inside the airbyte-server pod).

This script is intentionally self-contained (stdlib only) and talks to the Airbyte API
at http://localhost:8001.

It ensures:
- Instance is setup (initialSetupComplete = true)
- Custom declarative source definition exists (Connector Builder publish)
- Source exists with required injected manifest config
- Postgres destination exists
- Two connections exist (stations + readings)

It prints a single JSON object to stdout containing the created/ensured IDs.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, Optional


AIRBYTE_API_BASE = os.environ.get("AIRBYTE_API_BASE", "http://localhost:8001/api/v1").rstrip("/")
HTTP_TIMEOUT = int(os.environ.get("AIRBYTE_HTTP_TIMEOUT", "60"))

CONNECTOR_BUILDER_PROJECT_NAME = os.environ.get(
	"HYDRO_CONNECTOR_BUILDER_PROJECT_NAME", "uk_flood_monitoring_api"
)
SOURCE_DEFINITION_NAME = os.environ.get(
	"HYDRO_SOURCE_DEFINITION_NAME", "UK Flood Monitoring API (HydroLineage)"
)
SOURCE_DOCKER_IMAGE_TAG = os.environ.get("HYDRO_SOURCE_DOCKER_IMAGE_TAG", "7.6.3")
SOURCE_NAME = os.environ.get("HYDRO_SOURCE_NAME", "HydroLineage - UK Flood API")

DESTINATION_DEFINITION_ID = os.environ.get(
	"HYDRO_POSTGRES_DESTINATION_DEFINITION_ID",
	"25c5221d-dce2-4163-ade9-739ef790f503",  # Postgres destination
)
DESTINATION_NAME = os.environ.get("HYDRO_DESTINATION_NAME", "HydroLineage - Postgres (raw)")

POSTGRES_HOST = os.environ.get("HYDRO_POSTGRES_HOST")
POSTGRES_PORT = int(os.environ.get("HYDRO_POSTGRES_PORT", "5432"))
POSTGRES_DB = os.environ.get("HYDRO_POSTGRES_DB", "hydro")
POSTGRES_SCHEMA = os.environ.get("HYDRO_POSTGRES_SCHEMA", "raw")
POSTGRES_USERNAME = os.environ.get("HYDRO_POSTGRES_USERNAME", "postgres")
POSTGRES_PASSWORD = os.environ.get("HYDRO_POSTGRES_PASSWORD")

STATIONS_CONNECTION_NAME = os.environ.get(
	"HYDRO_STATIONS_CONNECTION_NAME", "HydroLineage - Stations -> Postgres"
)
READINGS_CONNECTION_NAME = os.environ.get(
	"HYDRO_READINGS_CONNECTION_NAME", "HydroLineage - Readings -> Postgres"
)


def _http_json(method: str, path: str, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
	url = f"{AIRBYTE_API_BASE}{path}"
	data = None
	headers = {"Accept": "application/json"}
	if body is not None:
		data = json.dumps(body).encode("utf-8")
		headers["Content-Type"] = "application/json"

	req = urllib.request.Request(url, data=data, headers=headers, method=method)
	try:
		with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
			raw = resp.read().decode("utf-8")
			if not raw:
				return {}
			return json.loads(raw)
	except urllib.error.HTTPError as e:
		raw = e.read().decode("utf-8") if hasattr(e, "read") else ""
		raise RuntimeError(f"Airbyte API {method} {path} failed: HTTP {e.code}: {raw}") from e


def _ensure_instance_setup() -> None:
	cfg = _http_json("GET", "/instance_configuration")
	if cfg.get("initialSetupComplete") is True:
		return

	_http_json(
		"POST",
		"/instance_configuration/setup",
		{
			"email": os.environ.get("HYDRO_AIRBYTE_SETUP_EMAIL", "hydrolineage@example.local"),
			"anonymousDataCollection": False,
			"initialSetupComplete": True,
			"displaySetupWizard": False,
		},
	)


def _get_default_user_id() -> str:
	cfg = _http_json("GET", "/instance_configuration")
	user_id = cfg.get("defaultUserId")
	if not user_id:
		raise RuntimeError(
			"Airbyte instance_configuration did not include defaultUserId; cannot discover workspace."
		)
	return str(user_id)


def _get_workspace_id(user_id: str) -> str:
	resp = _http_json("POST", "/workspaces/list_by_user_id", {"userId": user_id})
	workspaces = resp.get("workspaces") or []
	if not workspaces:
		raise RuntimeError(f"No workspaces found for userId={user_id}")
	return str(workspaces[0]["workspaceId"])


def _find_by_name(items: list[Dict[str, Any]], name: str) -> Optional[Dict[str, Any]]:
	for item in items:
		if item.get("name") == name:
			return item
	return None


def _list_source_definitions(workspace_id: str) -> list[Dict[str, Any]]:
	resp = _http_json("POST", "/source_definitions/list_for_workspace", {"workspaceId": workspace_id})
	return resp.get("sourceDefinitions") or []


def _create_and_publish_custom_source_definition(workspace_id: str, manifest: Dict[str, Any]) -> str:
	# Create a custom source definition directly (bypassing Connector Builder which is broken in Airbyte 2.0)
	# Use the declarative-manifest runner image with the manifest injected at runtime
	created = _http_json(
		"POST",
		"/source_definitions/create_custom",
		{
			"workspaceId": workspace_id,
			"sourceDefinition": {
				"name": SOURCE_DEFINITION_NAME,
				"dockerRepository": "airbyte/source-declarative-manifest",
				"dockerImageTag": SOURCE_DOCKER_IMAGE_TAG or "7.6.3",
				"documentationUrl": "https://docs.airbyte.com/integrations/sources/declarative-manifest",
			},
		},
	)
	source_definition_id = created.get("sourceDefinitionId")
	if not source_definition_id:
		raise RuntimeError(f"create_custom did not return sourceDefinitionId: {created}")

	return str(source_definition_id)


def _ensure_source_definition(workspace_id: str, manifest: Dict[str, Any]) -> str:
	existing = _find_by_name(_list_source_definitions(workspace_id), SOURCE_DEFINITION_NAME)
	if existing and existing.get("sourceDefinitionId"):
		source_definition_id = str(existing["sourceDefinitionId"])
		current_tag = existing.get("dockerImageTag")
		if SOURCE_DOCKER_IMAGE_TAG and current_tag != SOURCE_DOCKER_IMAGE_TAG:
			_http_json(
				"POST",
				"/source_definitions/update",
				{
					"workspaceId": workspace_id,
					"sourceDefinitionId": source_definition_id,
					"dockerImageTag": SOURCE_DOCKER_IMAGE_TAG,
				},
			)
		return source_definition_id

	source_definition_id = _create_and_publish_custom_source_definition(workspace_id, manifest)
	# Ensure the published definition runs the desired image tag.
	if SOURCE_DOCKER_IMAGE_TAG:
		_http_json(
			"POST",
			"/source_definitions/update",
			{
				"workspaceId": workspace_id,
				"sourceDefinitionId": source_definition_id,
				"dockerImageTag": SOURCE_DOCKER_IMAGE_TAG,
			},
		)
	return source_definition_id


def _list_sources(workspace_id: str) -> list[Dict[str, Any]]:
	resp = _http_json("POST", "/sources/list", {"workspaceId": workspace_id})
	return resp.get("sources") or []


def _ensure_source(workspace_id: str, source_definition_id: str, manifest: Dict[str, Any]) -> str:
	injected_config = {"__injected_declarative_manifest": manifest}

	existing = _find_by_name(_list_sources(workspace_id), SOURCE_NAME)
	if existing and existing.get("sourceId"):
		source_id = str(existing["sourceId"])
		_http_json(
			"POST",
			"/sources/update",
			{
				"sourceId": source_id,
				"name": SOURCE_NAME,
				"connectionConfiguration": injected_config,
			},
		)
		return source_id

	created = _http_json(
		"POST",
		"/sources/create",
		{
			"workspaceId": workspace_id,
			"name": SOURCE_NAME,
			"sourceDefinitionId": source_definition_id,
			"connectionConfiguration": injected_config,
		},
	)
	source_id = created.get("sourceId")
	if not source_id:
		raise RuntimeError(f"sources/create did not return sourceId: {created}")
	return str(source_id)


def _check_source(source_id: str) -> None:
	_http_json("POST", "/sources/check_connection", {"sourceId": source_id})


def _discover_source_schema(source_id: str) -> Dict[str, Any]:
	return _http_json("POST", "/sources/discover_schema", {"sourceId": source_id})


def _list_destinations(workspace_id: str) -> list[Dict[str, Any]]:
	resp = _http_json("POST", "/destinations/list", {"workspaceId": workspace_id})
	return resp.get("destinations") or []


def _ensure_destination(workspace_id: str) -> str:
	if not POSTGRES_HOST:
		raise RuntimeError("HYDRO_POSTGRES_HOST must be set")
	if POSTGRES_PASSWORD is None:
		raise RuntimeError("HYDRO_POSTGRES_PASSWORD must be set")

	existing = _find_by_name(_list_destinations(workspace_id), DESTINATION_NAME)

	config = {
		"host": POSTGRES_HOST,
		"port": POSTGRES_PORT,
		"database": POSTGRES_DB,
		"schema": POSTGRES_SCHEMA,
		"username": POSTGRES_USERNAME,
		"password": POSTGRES_PASSWORD,
		"ssl_mode": {"mode": "disable"},
	}

	if existing and existing.get("destinationId"):
		destination_id = str(existing["destinationId"])
		_http_json(
			"POST",
			"/destinations/update",
			{
				"destinationId": destination_id,
				"name": DESTINATION_NAME,
				"connectionConfiguration": config,
			},
		)
		return destination_id

	created = _http_json(
		"POST",
		"/destinations/create",
		{
			"workspaceId": workspace_id,
			"name": DESTINATION_NAME,
			"destinationDefinitionId": DESTINATION_DEFINITION_ID,
			"connectionConfiguration": config,
		},
	)
	destination_id = created.get("destinationId")
	if not destination_id:
		raise RuntimeError(f"destinations/create did not return destinationId: {created}")
	return str(destination_id)


def _list_connections(workspace_id: str) -> list[Dict[str, Any]]:
	resp = _http_json("POST", "/connections/list", {"workspaceId": workspace_id})
	return resp.get("connections") or []


def _build_single_stream_catalog(
	discovered: Dict[str, Any], stream_name: str, *, destination_sync_mode: str
) -> Dict[str, Any]:
	if "catalog" not in discovered or not isinstance(discovered["catalog"], dict):
		raise RuntimeError(f"Unexpected discover_schema response (missing catalog): {discovered}")

	streams = discovered["catalog"].get("streams") or []
	selected_stream = None
	for s in streams:
		st = (s or {}).get("stream") or {}
		if st.get("name") == stream_name:
			selected_stream = s
			break

	if not selected_stream:
		available = [((s.get("stream") or {}).get("name")) for s in streams]
		raise RuntimeError(f"Stream '{stream_name}' not found in discovered catalog. Available: {available}")

	return {
		"streams": [
			{
				"stream": selected_stream.get("stream"),
				"config": {
					"syncMode": "full_refresh",
					"destinationSyncMode": destination_sync_mode,
					"selected": True,
				},
			}
		]
	}


def _ensure_connection(
	workspace_id: str,
	*,
	name: str,
	source_id: str,
	destination_id: str,
	sync_catalog: Dict[str, Any],
) -> str:
	existing = _find_by_name(_list_connections(workspace_id), name)

	if existing and existing.get("connectionId"):
		connection_id = str(existing["connectionId"])
		_http_json(
			"POST",
			"/connections/update",
			{
				"connectionId": connection_id,
				"name": name,
				"status": "active",
				"syncCatalog": sync_catalog,
			},
		)
		return connection_id

	created = _http_json(
		"POST",
		"/connections/create",
		{
			"name": name,
			"sourceId": source_id,
			"destinationId": destination_id,
			"status": "active",
			"syncCatalog": sync_catalog,
			"namespaceDefinition": "destination",
			"scheduleType": "manual",
		},
	)

	connection_id = created.get("connectionId")
	if not connection_id:
		raise RuntimeError(f"connections/create did not return connectionId: {created}")
	return str(connection_id)


def _manifest() -> Dict[str, Any]:
	return {
		"type": "DeclarativeSource",
		"version": "0.29.0",
		"spec": {
			"type": "Spec",
			"connection_specification": {
				"type": "object",
				"required": [],
				"additionalProperties": True,
				"properties": {
					"api_key": {
						"type": "string",
						"title": "API Key (optional)",
						"description": "Optional API key for UK Flood Monitoring API",
						"airbyte_secret": True,
					}
				},
			},
		},
		"check": {"type": "CheckStream", "stream_names": ["stations"]},
		"streams": [
			{
				"type": "DeclarativeStream",
				"name": "stations",
				"retriever": {
					"type": "SimpleRetriever",
					"requester": {
						"type": "HttpRequester",
						"url_base": "https://environment.data.gov.uk/flood-monitoring/",
						"path": "id/stations",
						"request_parameters": {"_limit": "50"},
					},
					"record_selector": {
						"type": "RecordSelector",
						"extractor": {"type": "DpathExtractor", "field_path": ["items"]},
					},
				},
				"schema_loader": {
					"type": "InlineSchemaLoader",
					"schema": {
						"type": "object",
						"additionalProperties": True,
						"properties": {
							"@id": {"type": "string"},
							"RLOIid": {"type": "string"},
							"catchmentName": {"type": "string"},
							"dateOpened": {"type": "string"},
							"easting": {"type": ["number", "null"]},
							"label": {"type": "string"},
							"lat": {"type": "number"},
							"long": {"type": "number"},
							"northing": {"type": ["number", "null"]},
							"notation": {"type": "string"},
							"riverName": {"type": "string"},
							"stationReference": {"type": "string"},
							"status": {"type": "string"},
							"town": {"type": "string"},
							"wiskiID": {"type": "string"},
						},
					},
				},
			},
			{
				"type": "DeclarativeStream",
				"name": "water_level_readings",
				"retriever": {
					"type": "SimpleRetriever",
					"requester": {
						"type": "HttpRequester",
						"url_base": "https://environment.data.gov.uk/flood-monitoring/",
						"path": "id/measures",
						"request_parameters": {"_limit": "100", "parameter": "level"},
					},
					"record_selector": {
						"type": "RecordSelector",
						"extractor": {"type": "DpathExtractor", "field_path": ["items"]},
						"record_filter": {
							"type": "RecordFilter",
							"condition": "{{ record.get('latestReading') is not none }}",
						},
					},
				},
				"transformations": [
					{
						"type": "AddFields",
						"fields": [
							{"path": ["reading_id"], "value": "{{ record['latestReading']['@id'] }}"},
							{"path": ["station_id"], "value": "{{ record['stationReference'] }}"},
							{"path": ["measure_id"], "value": "{{ record['notation'] }}"},
							{"path": ["value"], "value": "{{ record['latestReading']['value'] }}"},
							{"path": ["reading_datetime"], "value": "{{ record['latestReading']['dateTime'] }}"},
						],
					},
					{
						"type": "RemoveFields",
						"field_pointers": [
							["@id"],
							["datumType"],
							["label"],
							["latestReading"],
							["notation"],
							["parameter"],
							["parameterName"],
							["period"],
							["qualifier"],
							["station"],
							["stationReference"],
							["unit"],
							["unitName"],
							["valueType"],
						],
					},
				],
				"schema_loader": {
					"type": "InlineSchemaLoader",
					"schema": {
						"type": "object",
						"additionalProperties": True,
						"properties": {
							"reading_id": {"type": "string"},
							"station_id": {"type": "string"},
							"measure_id": {"type": "string"},
							"value": {"type": "number"},
							"reading_datetime": {"type": "string"},
						},
					},
				},
			},
		],
	}


def main() -> int:
	_ensure_instance_setup()
	user_id = _get_default_user_id()
	workspace_id = _get_workspace_id(user_id)

	manifest = _manifest()

	source_definition_id = _ensure_source_definition(workspace_id, manifest)
	source_id = _ensure_source(workspace_id, source_definition_id, manifest)

	_check_source(source_id)
	discovered = _discover_source_schema(source_id)

	destination_id = _ensure_destination(workspace_id)

	# Use "append" mode to avoid dropping tables that have dependent dbt views
	stations_catalog = _build_single_stream_catalog(discovered, "stations", destination_sync_mode="append")
	readings_catalog = _build_single_stream_catalog(discovered, "water_level_readings", destination_sync_mode="append")

	stations_connection_id = _ensure_connection(
		workspace_id,
		name=STATIONS_CONNECTION_NAME,
		source_id=source_id,
		destination_id=destination_id,
		sync_catalog=stations_catalog,
	)
	readings_connection_id = _ensure_connection(
		workspace_id,
		name=READINGS_CONNECTION_NAME,
		source_id=source_id,
		destination_id=destination_id,
		sync_catalog=readings_catalog,
	)

	print(
		json.dumps(
			{
				"workspace_id": workspace_id,
				"source_definition_id": source_definition_id,
				"source_id": source_id,
				"destination_id": destination_id,
				"stations_connection_id": stations_connection_id,
				"readings_connection_id": readings_connection_id,
			}
		)
	)
	return 0


if __name__ == "__main__":
	try:
		raise SystemExit(main())
	except Exception as e:
		print(f"ERROR: {e}", file=sys.stderr)
		raise
