# SPDX-License-Identifier: Apache-2.0
#
# © Crown Copyright 2025. This work has been developed by the National Digital Twin
# Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
# entity

from __future__ import annotations

from dataclasses import dataclass
import logging
import re
from typing import Iterable, List, Optional

import requests

logger = logging.getLogger(__name__)


def _make_data_platform_urn(platform: str) -> str:
    return f"urn:li:dataPlatform:{platform}"

from datahub.emitter.mce_builder import (
    make_data_flow_urn,
    make_data_job_urn,
    make_dataset_urn,
)
from datahub.ingestion.api.source import Source, SourceReport
try:
    from datahub.ingestion.api.workunit import MetadataWorkUnit  # type: ignore
except ImportError:  # pragma: no cover - older DataHub versions
    from datahub.ingestion.extractor.mce_extractor import (  # type: ignore
        MetadataWorkUnit,
    )
from datahub.metadata.schema_classes import (
    DataFlowInfoClass,
    DataFlowSnapshotClass,
    DataJobInputOutputClass,
    DataJobInfoClass,
    DataJobSnapshotClass,
    DatasetPropertiesClass,
    DatasetSnapshotClass,
    MetadataChangeEventClass,
    SchemaFieldClass,
    SchemaFieldDataTypeClass,
    SchemaMetadataClass,
    StringTypeClass,
    NumberTypeClass,
    BooleanTypeClass,
    UpstreamClass,
    UpstreamLineageClass,
)

try:  # Optional classes vary by DataHub ingestion version
    from datahub.metadata.schema_classes import (  # type: ignore
        DateTypeClass,
        TimeTypeClass,
        DateTimeTypeClass,
        TimestampTypeClass,
        BytesTypeClass,
        UpstreamLineageTypeClass,
    )
except ImportError:  # pragma: no cover - fallback for older versions
    DateTypeClass = None  # type: ignore
    TimeTypeClass = None  # type: ignore
    DateTimeTypeClass = None  # type: ignore
    TimestampTypeClass = None  # type: ignore
    BytesTypeClass = None  # type: ignore
    UpstreamLineageTypeClass = None  # type: ignore

try:  # Optional schema holders (may vary independently)
    from datahub.metadata.schema_classes import PlatformSchemaClass  # type: ignore
except ImportError:  # pragma: no cover
    PlatformSchemaClass = None  # type: ignore

try:  # Optional schema holders (may vary independently)
    from datahub.metadata.schema_classes import (  # type: ignore
        OtherSchemaClass,
        SchemalessClass,
    )
except ImportError:  # pragma: no cover
    OtherSchemaClass = None  # type: ignore
    SchemalessClass = None  # type: ignore


@dataclass
class AirbyteSourceConfig:
    host_port: str
    username: Optional[str] = None
    password: Optional[str] = None
    env: str = "PROD"
    emit_source_datasets: bool = False
    strip_database_prefix_from_namespace: bool = True


class AirbyteSource(Source):
    def __init__(self, config: AirbyteSourceConfig, ctx) -> None:
        super().__init__(ctx)
        self.config = config
        self.report = SourceReport()
        scheme = "http" if "http" not in config.host_port else ""
        base = config.host_port
        if scheme:
            base = f"{scheme}://{base}"
        self.base_url = base.rstrip("/")
        self.auth = (
            (config.username, config.password)
            if config.username or config.password
            else None
        )

    @classmethod
    def create(cls, config_dict, ctx):
        config = AirbyteSourceConfig(**config_dict)
        return cls(config, ctx)

    def _list_connections(self) -> List[dict]:
        url = f"{self.base_url}/api/public/v1/connections"
        resp = requests.get(url, timeout=30, auth=self.auth)
        resp.raise_for_status()
        payload = resp.json()
        return payload.get("data", [])

    def _get_connection_details(self, connection_id: str) -> Optional[dict]:
        public_url = f"{self.base_url}/api/public/v1/connections/{connection_id}"
        resp = requests.get(public_url, timeout=30, auth=self.auth)
        if resp.status_code == 200:
            return resp.json()
        url = f"{self.base_url}/api/v1/connections/get"
        resp = requests.post(
            url,
            json={"connectionId": connection_id},
            timeout=30,
            auth=self.auth,
        )
        resp.raise_for_status()
        return resp.json()

    def _get_destination_details(self, destination_id: str) -> Optional[dict]:
        url = f"{self.base_url}/api/v1/destinations/get"
        resp = requests.post(
            url,
            json={"destinationId": destination_id},
            timeout=30,
            auth=self.auth,
        )
        resp.raise_for_status()
        return resp.json()

    def _schema_type_from_json(self, field_schema: dict) -> SchemaFieldDataTypeClass:
        json_type = field_schema.get("type")
        if isinstance(json_type, list):
            json_type = next((item for item in json_type if item != "null"), None)

        fmt = field_schema.get("format")
        if fmt == "date-time":
            if DateTimeTypeClass is not None:
                return SchemaFieldDataTypeClass(type=DateTimeTypeClass())
            if TimestampTypeClass is not None:
                return SchemaFieldDataTypeClass(type=TimestampTypeClass())
        if fmt == "date" and DateTypeClass is not None:
            return SchemaFieldDataTypeClass(type=DateTypeClass())
        if fmt == "time" and TimeTypeClass is not None:
            return SchemaFieldDataTypeClass(type=TimeTypeClass())

        if json_type in {"integer", "number"}:
            return SchemaFieldDataTypeClass(type=NumberTypeClass())
        if json_type == "boolean":
            return SchemaFieldDataTypeClass(type=BooleanTypeClass())
        if json_type == "string":
            return SchemaFieldDataTypeClass(type=StringTypeClass())
        if json_type == "bytes" and BytesTypeClass is not None:
            return SchemaFieldDataTypeClass(type=BytesTypeClass())

        return SchemaFieldDataTypeClass(type=StringTypeClass())

    def _build_schema_fields(self, json_schema: dict) -> List[SchemaFieldClass]:
        if not isinstance(json_schema, dict):
            return []

        properties = json_schema.get("properties")
        if not isinstance(properties, dict):
            return []

        fields: List[SchemaFieldClass] = []
        for field_name, field_schema in properties.items():
            if not isinstance(field_schema, dict):
                continue
            sanitized_name = re.sub(r"[^A-Za-z0-9_]", "_", field_name)
            if not sanitized_name:
                continue
            if sanitized_name[0].isdigit():
                sanitized_name = f"_{sanitized_name}"
            field_type = self._schema_type_from_json(field_schema)
            json_type = field_schema.get("type")
            if isinstance(json_type, list):
                nullable = "null" in json_type
            else:
                nullable = json_type == "null"
            fields.append(
                SchemaFieldClass(
                    fieldPath=sanitized_name,
                    type=field_type,
                    description=field_schema.get("description"),
                    nativeDataType=str(field_schema.get("type") or ""),
                    nullable=nullable,
                )
            )
        return fields

    def get_workunits(self) -> Iterable[MetadataWorkUnit]:
        connections = self._list_connections()
        logger.info(f"\n{'='*60}")
        logger.info(f"Airbyte Metadata Ingestion Starting")
        logger.info(f"Found {len(connections)} connection(s) in Airbyte")
        logger.info(f"emit_source_datasets: {self.config.emit_source_datasets}")
        logger.info(f"{'='*60}\n")
        print("Airbyte Metadata Ingestion Starting")
        print(f"Found {len(connections)} connection(s) in Airbyte")
        print(f"emit_source_datasets: {self.config.emit_source_datasets}")
        for conn in connections:
            connection_id = conn.get("connectionId") or conn.get("connection_id")
            name = conn.get("name") or connection_id
            if not connection_id:
                continue

            flow_urn = make_data_flow_urn("airbyte", connection_id, self.config.env)
            logger.info(f"Creating DataFlow: {flow_urn} (name={name})")
            flow_info = DataFlowInfoClass(
                name=name,
                description=f"Airbyte connection {name}",
                project="airbyte",
            )
            flow_snapshot = DataFlowSnapshotClass(urn=flow_urn, aspects=[flow_info])
            flow_mce = MetadataChangeEventClass(proposedSnapshot=flow_snapshot)
            logger.info(f"  ✅ Emitting DataFlow metadata for {name}")
            yield MetadataWorkUnit(id=f"airbyte-flow-{connection_id}", mce=flow_mce)

            job_urn = make_data_job_urn(
                orchestrator="airbyte",
                flow_id=connection_id,
                job_id=connection_id,
            )
            logger.info(f"Creating DataJob: {job_urn}")
            try:
                job_info = DataJobInfoClass(
                    name=name,
                    description=f"Airbyte connection {name}",
                    type="AIRBYTE",
                    flowUrn=flow_urn,
                )
            except Exception:  # noqa: BLE001
                job_info = DataJobInfoClass(
                    name=name,
                    description=f"Airbyte connection {name}",
                    type="AIRBYTE",
                )

            try:
                connection_details = self._get_connection_details(connection_id)
            except Exception as exc:  # noqa: BLE001
                self.report.report_warning(
                    key=f"connection-details-{connection_id}",
                    reason=f"Failed to load Airbyte connection details: {exc}",
                )
                continue

            destination_id = connection_details.get("destinationId")
            destination_details = None
            if destination_id:
                try:
                    destination_details = self._get_destination_details(destination_id)
                except Exception as exc:  # noqa: BLE001
                    self.report.report_warning(
                        key=f"destination-details-{destination_id}",
                        reason=f"Failed to load Airbyte destination details: {exc}",
                    )

            destination_config = (destination_details or {}).get(
                "connectionConfiguration", {}
            )
            destination_db = destination_config.get("database")
            destination_schema = destination_config.get("schema") or "public"
            logger.info(
                "Connection %s destination: db=%s schema=%s",
                connection_id,
                destination_db,
                destination_schema,
            )
            print(
                f"Connection {connection_id} destination: db={destination_db} schema={destination_schema}"
            )

            sync_catalog = connection_details.get("syncCatalog", {})
            streams = sync_catalog.get("streams", [])
            logger.info(
                "Connection %s syncCatalog streams: %s",
                connection_id,
                len(streams) if isinstance(streams, list) else "n/a",
            )
            print(
                f"Connection {connection_id} syncCatalog streams: "
                f"{len(streams) if isinstance(streams, list) else 'n/a'}"
            )
            if not streams:
                config_streams = (
                    connection_details.get("configurations", {}).get("streams", [])
                )
                logger.info(
                    "Connection %s configurations streams: %s",
                    connection_id,
                    len(config_streams) if isinstance(config_streams, list) else "n/a",
                )
                print(
                    f"Connection {connection_id} configurations streams: "
                    f"{len(config_streams) if isinstance(config_streams, list) else 'n/a'}"
                )
                if isinstance(config_streams, list):
                    streams = [
                        {
                            "stream": {
                                "name": stream.get("name"),
                                "namespace": destination_schema,
                                "jsonSchema": {},
                            }
                        }
                        for stream in config_streams
                        if isinstance(stream, dict) and stream.get("name")
                    ]
            if not isinstance(streams, list):
                continue
            if not streams:
                logger.warning(
                    "Connection %s has no streams in syncCatalog/configurations.",
                    connection_id,
                )
                print(f"Connection {connection_id} has no streams to emit.")

            input_datasets: List[str] = []
            output_datasets: List[str] = []

            for stream in streams:
                stream_def = stream.get("stream", {})
                if not isinstance(stream_def, dict):
                    continue

                stream_name = stream_def.get("name")
                if not stream_name:
                    continue

                stream_schema = stream_def.get("jsonSchema", {})
                schema_name = stream_def.get("namespace") or destination_schema
                if (
                    self.config.strip_database_prefix_from_namespace
                    and destination_db
                    and isinstance(schema_name, str)
                    and schema_name.startswith(f"{destination_db}.")
                ):
                    schema_name = schema_name[len(destination_db) + 1 :]
                dataset_name = (
                    f"{destination_db}.{schema_name}.{stream_name}"
                    if destination_db
                    else f"{schema_name}.{stream_name}"
                )

                destination_urn = make_dataset_urn(
                    "postgres",
                    dataset_name,
                    self.config.env,
                )
                output_datasets.append(destination_urn)
                logger.info("  Processing stream: %s → %s", stream_name, dataset_name)
                logger.info("    Destination URN: %s", destination_urn)
                print(f"Stream {stream_name} → {dataset_name}")
                print(f"  Destination URN: {destination_urn}")
                logger.info("  Processing stream: %s → %s", stream_name, dataset_name)
                logger.info("    Destination URN: %s", destination_urn)
                source_urn = None
                if self.config.emit_source_datasets:
                    source_urn = make_dataset_urn(
                        "airbyte",
                        f"{connection_id}.{stream_name}",
                        self.config.env,
                    )
                    input_datasets.append(source_urn)
                    logger.info("    Source URN: %s", source_urn)
                    print(f"  Source URN: {source_urn}")

                schema_fields = self._build_schema_fields(stream_schema)
                if PlatformSchemaClass is not None:
                    platform_schema = PlatformSchemaClass(
                        rawSchema=str(stream_schema)
                    )
                elif OtherSchemaClass is not None:
                    platform_schema = OtherSchemaClass(rawSchema=str(stream_schema))
                elif SchemalessClass is not None:
                    platform_schema = SchemalessClass()
                else:
                    platform_schema = None

                emit_destination_schema = len(schema_fields) > 0
                destination_schema_metadata = None
                if emit_destination_schema:
                    destination_schema_metadata = SchemaMetadataClass(
                        schemaName=dataset_name,
                        platform=_make_data_platform_urn("postgres"),
                        version=0,
                        hash="",
                        fields=schema_fields,
                        platformSchema=platform_schema,
                    )
                source_schema_metadata = None
                if self.config.emit_source_datasets:
                    source_schema_metadata = SchemaMetadataClass(
                        schemaName=f"{connection_id}.{stream_name}",
                        platform=_make_data_platform_urn("airbyte"),
                        version=0,
                        hash="",
                        fields=schema_fields,
                        platformSchema=platform_schema,
                    )

                destination_properties = DatasetPropertiesClass(
                    name=dataset_name,
                    description=f"Airbyte output dataset for {stream_name}",
                )
                source_properties = None
                if self.config.emit_source_datasets:
                    source_properties = DatasetPropertiesClass(
                        name=f"{connection_id}.{stream_name}",
                        description=f"Airbyte source stream for {stream_name}",
                    )

                if UpstreamLineageTypeClass is not None:
                    upstream_type = UpstreamLineageTypeClass.TRANSFORMED
                else:
                    upstream_type = "TRANSFORMED"

                upstream_lineage = None
                if self.config.emit_source_datasets and source_urn:
                    upstream = UpstreamClass(
                        dataset=source_urn,
                        type=upstream_type,
                    )
                    upstream_lineage = UpstreamLineageClass(upstreams=[upstream])

                    source_snapshot = DatasetSnapshotClass(
                        urn=source_urn,
                        aspects=[source_properties, source_schema_metadata],
                    )
                    source_mce = MetadataChangeEventClass(
                        proposedSnapshot=source_snapshot
                    )
                    logger.info("    ✅ Emitting source dataset: %s", source_urn)
                    yield MetadataWorkUnit(
                        id=f"airbyte-source-dataset-{connection_id}-{stream_name}",
                        mce=source_mce,
                    )

                destination_aspects = [destination_properties]
                if destination_schema_metadata is not None:
                    destination_aspects.append(destination_schema_metadata)
                if upstream_lineage is not None:
                    destination_aspects.append(upstream_lineage)

                destination_snapshot = DatasetSnapshotClass(
                    urn=destination_urn,
                    aspects=destination_aspects,
                )
                destination_mce = MetadataChangeEventClass(
                    proposedSnapshot=destination_snapshot
                )
                if destination_schema_metadata is None:
                    logger.info(
                        "    ⚠️ Skipping destination schema emission for %s (no fields)",
                        destination_urn,
                    )
                logger.info("    ✅ Emitting destination dataset: %s", destination_urn)
                if upstream_lineage:
                    logger.info("    📊 With upstream lineage from: %s", source_urn)
                if destination_schema_metadata is not None:
                    logger.info("    Schema fields: %s fields", len(schema_fields))
                yield MetadataWorkUnit(
                    id=f"airbyte-destination-dataset-{connection_id}-{stream_name}",
                    mce=destination_mce,
                )

            job_aspects = [job_info]
            logger.info(
                "  📌 DataJob output count: %s",
                len(output_datasets),
            )
            print(f"DataJob output count: {len(output_datasets)}")
            if output_datasets:
                logger.info(
                    "  📌 DataJob inputs: %s",
                    input_datasets if input_datasets else "[]",
                )
                logger.info(
                    "  📌 DataJob outputs: %s",
                    output_datasets,
                )
                job_aspects.append(
                    DataJobInputOutputClass(
                        inputDatasets=input_datasets,
                        outputDatasets=output_datasets,
                    )
                )
                print(f"DataJob outputs: {output_datasets}")

            job_snapshot = DataJobSnapshotClass(urn=job_urn, aspects=job_aspects)
            job_mce = MetadataChangeEventClass(proposedSnapshot=job_snapshot)
            logger.info("  ✅ Emitting DataJob metadata (flowUrn=%s)", flow_urn)
            if output_datasets:
                logger.info(
                    "  📊 DataJob outputs: %s dataset(s)",
                    len(output_datasets),
                )
            yield MetadataWorkUnit(id=f"airbyte-job-{connection_id}", mce=job_mce)

    def get_report(self):
        return self.report

    def infer_platform(self):
        return "airbyte"
