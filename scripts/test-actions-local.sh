#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
#
# Local simulation of the CI smoke-test quickstart, scoped to just the
# datahub-actions container so you can reproduce exit-code 123 without a
# 45-minute CI cycle.
#
# USAGE:
#   ./scripts/test-actions-local.sh            # build + run full quickstart
#   ./scripts/test-actions-local.sh --quick    # skip full stack, run actions CLI directly
#   ./scripts/test-actions-local.sh --build-only  # build image but don't start anything
#
# PREREQUISITES:
#   docker buildx, docker compose v2, ~2 GB free (build layer cache)
#   All other images already pulled (run once: docker pull acryldata/... manually if needed)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

###############################################################################
# Config — must match the cached image versions already on disk
###############################################################################
DATAHUB_REPO="acryldata"
DATAHUB_VERSION="vbbf27a4-SNAPSHOT"    # ← must match existing docker images tag
RELEASE_VERSION="1.4.0.2"             # PEP 440; must match cliVersion.gradle
BUNDLED_CLI_VERSION="1.4.0.2"
TARGET_IMAGE="${DATAHUB_REPO}/datahub-actions:${DATAHUB_VERSION}-slim"

MODE="${1:-}"

###############################################################################
# Phase 1: Build just the datahub-actions slim image
###############################################################################
build_image() {
  echo ""
  echo "╔══════════════════════════════════════════════════════════════╗"
  echo "║  Building datahub-actions:${DATAHUB_VERSION}-slim (local)         ║"
  echo "╚══════════════════════════════════════════════════════════════╝"
  echo ""

  cd "$REPO_ROOT"

  # Use docker buildx directly — faster than invoking Gradle for a single image.
  # Build context is the repo root (Dockerfile references metadata-ingestion/ etc.)
  docker buildx build \
    --file docker/datahub-actions/Dockerfile \
    --target final-slim \
    --build-arg "RELEASE_VERSION=${RELEASE_VERSION}" \
    --build-arg "BUNDLED_CLI_VERSION=${BUNDLED_CLI_VERSION}" \
    --build-arg "BUNDLED_VENV_SLIM_MODE=true" \
    --build-arg "APP_ENV=slim" \
    --tag "${TARGET_IMAGE}" \
    --load \
    .

  echo ""
  echo "✓ Built: ${TARGET_IMAGE}"
  echo ""
}

###############################################################################
# Phase 2 (--quick): Run the datahub-actions CLI directly inside the container,
# bypassing dockerize and the compose stack entirely.
# Useful to see Python import errors / config errors within ~5 seconds.
###############################################################################
quick_test() {
  local image="${1:-${TARGET_IMAGE}}"
  echo ""
  echo "╔══════════════════════════════════════════════════════════════╗"
  echo "║  Quick test: running datahub-actions CLI in isolation        ║"
  echo "╚══════════════════════════════════════════════════════════════╝"
  echo "  Image: ${image}"
  echo "  (No GMS / Kafka needed — this just exercises Python startup) "
  echo ""

  docker run --rm \
    -e DATAHUB_GMS_HOST=localhost \
    -e DATAHUB_GMS_PORT=8080 \
    -e KAFKA_BOOTSTRAP_SERVER=localhost:9092 \
    -e SCHEMA_REGISTRY_URL="http://localhost:8081" \
    -e DATAHUB_SYSTEM_CLIENT_ID="__datahub_system" \
    -e DATAHUB_SYSTEM_CLIENT_SECRET="JohnSnowKnowsNothing" \
    -e EXECUTOR_ID="default" \
    --entrypoint /bin/bash \
    "${image}" \
    -c '
      echo "=== Python version ==="
      python --version
      echo ""
      echo "=== datahub-actions version ==="
      datahub-actions version 2>&1 || true
      echo ""
      echo "=== Running actions CLI (Kafka connection will fail - that is expected) ==="
      timeout 30 datahub-actions actions --debug \
        -c /etc/datahub/actions/system/conf/executor.yaml \
        2>&1 || true
      echo ""
      echo "=== Exit code captured above ==="
    '
}

###############################################################################
# Phase 2 (default): Run the full quickstart compose stack
###############################################################################
full_test() {
  echo ""
  echo "╔══════════════════════════════════════════════════════════════╗"
  echo "║  Starting full quickstart-consumers stack                    ║"
  echo "╚══════════════════════════════════════════════════════════════╝"
  echo "  Using pre-built cached images for all services except actions"
  echo "  Actions image: ${TARGET_IMAGE} (locally built)"
  echo ""

  cd "$REPO_ROOT"

  # Run quickstart (same env vars as CI)
  DATAHUB_REPO="${DATAHUB_REPO}" \
  DATAHUB_VERSION="${DATAHUB_VERSION}" \
  DATAHUB_ACTIONS_IMAGE="${DATAHUB_REPO}/datahub-actions" \
  DATAHUB_TELEMETRY_ENABLED=false \
  ACTIONS_EXTRA_PACKAGES="" \
  ACTIONS_CONFIG="file:///etc/datahub/actions/system/conf/executor.yaml" \
  DATAHUB_LOCAL_ACTIONS_ENV="${REPO_ROOT}/smoke-test/test_resources/actions/actions.env" \
    docker compose \
      --project-directory docker/profiles \
      --profile quickstart-consumers \
      up -d --wait --wait-timeout 300

  echo ""
  echo "╔══════════════════════════════════════════════════════════════╗"
  echo "║  Stack is up — following datahub-actions logs (Ctrl-C to stop) ║"
  echo "╚══════════════════════════════════════════════════════════════╝"
  echo ""

  # Follow the actions container logs so we see the crash in real time
  CONTAINER="$(docker ps -aq --filter name=datahub-actions | head -1)"
  if [ -n "$CONTAINER" ]; then
    docker logs -f "$CONTAINER" 2>&1
    EXIT_CODE="$(docker inspect "$CONTAINER" --format='{{.State.ExitCode}}')"
    echo ""
    echo "=== Container exited with code: ${EXIT_CODE} ==="
  else
    echo "WARNING: datahub-actions container not found"
    docker ps -a
  fi
}

cleanup() {
  echo ""
  echo "--- Cleaning up containers ---"
  cd "$REPO_ROOT"
  DATAHUB_REPO="${DATAHUB_REPO}" DATAHUB_VERSION="${DATAHUB_VERSION}" \
    docker compose \
      --project-directory docker/profiles \
      --profile quickstart-consumers \
      down -v 2>/dev/null || true
}

###############################################################################
# Main
###############################################################################
if [[ "$MODE" == "--quick" ]]; then
  build_image
  quick_test "${TARGET_IMAGE}"
elif [[ "$MODE" == "--no-build" ]]; then
  # Fastest: use the already-cached image to check if the crash reproduces as-is
  CACHED="acryldata/datahub-actions:${DATAHUB_VERSION}-slim"
  echo "Skipping build — testing cached image: ${CACHED}"
  quick_test "${CACHED}"
elif [[ "$MODE" == "--build-only" ]]; then
  build_image
  echo "Image built. Run without --build-only to start the stack."
else
  trap cleanup EXIT
  build_image
  full_test
fi
