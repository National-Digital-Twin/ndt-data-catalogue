# SPDX-License-Identifier: Apache-2.0
#
# © Crown Copyright 2025. This work has been developed by the National Digital Twin
# Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
# entity

FROM acryldata/datahub-ingestion:latest

WORKDIR /opt/datahub/custom

USER root
RUN python -m pip install --no-cache-dir --upgrade pip && \
	python -m pip install --no-cache-dir --upgrade "acryl-datahub[airbyte]"
USER datahub

COPY pyproject.toml /opt/datahub/custom/pyproject.toml
COPY datahub_airbyte_source /opt/datahub/custom/datahub_airbyte_source

RUN python -m pip install --no-cache-dir /opt/datahub/custom

# Use the base image entrypoint/cmd
