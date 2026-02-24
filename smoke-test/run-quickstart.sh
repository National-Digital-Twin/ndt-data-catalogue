#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
#
# This file is unmodified from its original version developed by Acryl Data, Inc.,
# and is now included as part of a repository maintained by the National Digital Twin Programme.
# All support, maintenance and further development of this code is now the responsibility
# of the National Digital Twin Programme.

set -euxo pipefail

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

../gradlew :smoke-test:installDev
set +x
echo "Activating virtual environment"
source venv/bin/activate
set -x

mkdir -p ~/.datahub/plugins/frontend/auth/
echo "test_user:test_pass" >> ~/.datahub/plugins/frontend/auth/user.props

echo "DATAHUB_VERSION = $DATAHUB_VERSION"
DATAHUB_SEARCH_IMAGE="${DATAHUB_SEARCH_IMAGE:=opensearchproject/opensearch}"
DATAHUB_SEARCH_TAG="${DATAHUB_SEARCH_TAG:=2.19.3}"
XPACK_SECURITY_ENABLED="${XPACK_SECURITY_ENABLED:=plugins.security.disabled=true}"
ELASTICSEARCH_USE_SSL="${ELASTICSEARCH_USE_SSL:=false}"
USE_AWS_ELASTICSEARCH="${USE_AWS_ELASTICSEARCH:=true}"

# For smoke tests, run all system actions (including doc propagation) by default
# for non-cypress runs. Keep cypress behavior unchanged unless explicitly
# overridden via SMOKE_TEST_ACTIONS_CONFIG.
SMOKE_TEST_ACTIONS_CONFIG="${SMOKE_TEST_ACTIONS_CONFIG:-}"
if [ -n "${SMOKE_TEST_ACTIONS_CONFIG}" ]; then
	ACTIONS_CONFIG_VALUE="${SMOKE_TEST_ACTIONS_CONFIG}"
elif [ "${TEST_STRATEGY:-}" = "cypress" ]; then
	ACTIONS_CONFIG_VALUE="${ACTIONS_CONFIG:-}"
else
	ACTIONS_CONFIG_VALUE=""
fi

THEME_V2_DEFAULT=false \
SHOW_HAS_SIBLINGS_FILTER=false \
SHOW_SEARCH_BAR_AUTOCOMPLETE_REDESIGN=false \
SHOW_INGESTION_PAGE_REDESIGN=true \
SHOW_HOME_PAGE_REDESIGN=true \
SEARCH_BAR_API_VARIANT=AUTOCOMPLETE_FOR_MULTIPLE \
DATAHUB_TELEMETRY_ENABLED=false \
DOCKER_COMPOSE_BASE="file://$( dirname "$DIR" )" \
DATAHUB_SEARCH_IMAGE="$DATAHUB_SEARCH_IMAGE" DATAHUB_SEARCH_TAG="$DATAHUB_SEARCH_TAG" \
XPACK_SECURITY_ENABLED="$XPACK_SECURITY_ENABLED" ELASTICSEARCH_USE_SSL="$ELASTICSEARCH_USE_SSL" \
USE_AWS_ELASTICSEARCH="$USE_AWS_ELASTICSEARCH" \
DATAHUB_VERSION=${DATAHUB_VERSION} \
ELASTICSEARCH_INDEX_BUILDER_REFRESH_INTERVAL_SECONDS=1 \
POLICY_CACHE_REFRESH_INTERVAL_SECONDS=10 \
ACTIONS_CONFIG="${ACTIONS_CONFIG_VALUE}" \
DATAHUB_ACTIONS_IMAGE="${DATAHUB_ACTIONS_IMAGE:-${DATAHUB_REPO:-acryldata}/datahub-actions}" \
DATAHUB_LOCAL_ACTIONS_ENV=`pwd`/test_resources/actions/actions.env  \
docker compose --project-directory ../docker/profiles --profile ${PROFILE_NAME:-quickstart-consumers} up -d --quiet-pull --wait --wait-timeout 900

