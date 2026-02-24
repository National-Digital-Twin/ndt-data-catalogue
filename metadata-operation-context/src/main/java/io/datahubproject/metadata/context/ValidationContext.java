/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

package io.datahubproject.metadata.context;

import java.util.Optional;
import lombok.Builder;
import lombok.Getter;

/** Context holder for environment variables relevant to operations */
@Builder(toBuilder = true)
@Getter
public class ValidationContext implements ContextInterface {
  // Uses alternate validation flow for MCP ingestion
  private final boolean alternateValidation;

  // Flag to indicate this is a remediation deletion (skip size validation to prevent circular
  // validation)
  private final boolean isRemediationDeletion;

  @Override
  public Optional<Integer> getCacheKeyComponent() {
    return Optional.of((alternateValidation ? 1 : 0) + (isRemediationDeletion ? 2 : 0));
  }
}
