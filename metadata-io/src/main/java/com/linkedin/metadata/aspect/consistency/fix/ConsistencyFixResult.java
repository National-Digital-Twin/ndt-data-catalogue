/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

package com.linkedin.metadata.aspect.consistency.fix;

import java.util.List;
import javax.annotation.Nonnull;
import lombok.Builder;
import lombok.Data;

/** Result of a fix operation, containing details about all fixes applied. */
@Data
@Builder
public class ConsistencyFixResult {

  /** Whether this was a dry-run (no actual changes made) */
  private final boolean dryRun;

  /** Total number of issues processed */
  private final int totalProcessed;

  /** Number of entities successfully fixed (or would be fixed in dry-run) */
  private final int entitiesFixed;

  /** Number of entities that failed to fix */
  private final int entitiesFailed;

  /** Details of each fix operation */
  @Nonnull private final List<ConsistencyFixDetail> fixDetails;
}
