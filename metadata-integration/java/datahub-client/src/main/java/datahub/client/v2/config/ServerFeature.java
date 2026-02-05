/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

package datahub.client.v2.config;

/**
 * Features that may be supported by a DataHub server.
 *
 * <p>Features can be detected through:
 *
 * <ul>
 *   <li>Config flags (e.g., patchCapable: true/false)
 *   <li>Version thresholds (e.g., OpenAPI requires Core >= 1.0.1 or Cloud >= 0.3.11)
 * </ul>
 */
public enum ServerFeature {
  /** Server supports JSON patch operations for metadata updates */
  PATCH_CAPABLE,

  /** Server supports stateful ingestion for incremental metadata updates */
  STATEFUL_INGESTION,

  /** Server supports impact analysis features */
  IMPACT_ANALYSIS,

  /** Server supports OpenAPI endpoints (alternative to RestLI) */
  OPENAPI_SDK,

  /** Server supports async API tracing for request tracking */
  API_TRACING,

  /** Server is running DataHub Cloud (vs self-hosted) */
  DATAHUB_CLOUD
}
