/*
 * SPDX-License-Identifier: Apache-2.0
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

package com.linkedin.metadata.config;

import lombok.Data;

/**
 * Validation configuration for DataHub operations.
 *
 * <p>All defaults are specified in application.yaml via environment variables. No defaults in Java
 * code to avoid confusion when values become null unexpectedly during config refresh.
 */
@Data
public class ValidationConfiguration {
  /** Aspect size validation configuration (applies to ALL aspect writes: REST/GraphQL/MCP) */
  private AspectSizeValidationConfiguration aspectSize;
}
