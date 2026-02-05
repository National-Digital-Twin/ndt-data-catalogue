/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

package com.linkedin.metadata.aspect.consistency.fix;

import com.linkedin.metadata.aspect.consistency.ConsistencyIssue;
import io.datahubproject.metadata.context.OperationContext;
import javax.annotation.Nonnull;

/**
 * Interface for applying fixes to resolve consistency issues.
 *
 * <p>Each implementation handles a specific {@link ConsistencyFixType}. The fix uses data from the
 * {@link ConsistencyIssue} to perform the necessary operations.
 *
 * <p>Implementations should be stateless and thread-safe.
 */
public interface ConsistencyFix {

  /**
   * Get the fix type this implementation handles.
   *
   * @return fix type
   */
  @Nonnull
  ConsistencyFixType getType();

  /**
   * Apply the fix for an issue.
   *
   * @param opContext operation context
   * @param issue the issue to fix (contains all necessary data)
   * @param dryRun if true, only report what would be done without making changes
   * @return detail of the fix operation
   */
  @Nonnull
  ConsistencyFixDetail apply(
      @Nonnull OperationContext opContext, @Nonnull ConsistencyIssue issue, boolean dryRun);
}
