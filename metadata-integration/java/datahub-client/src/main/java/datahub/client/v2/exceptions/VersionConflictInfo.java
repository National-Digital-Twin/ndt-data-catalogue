/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

package datahub.client.v2.exceptions;

import com.linkedin.mxe.MetadataChangeProposal;
import javax.annotation.Nonnull;
import javax.annotation.Nullable;
import lombok.Value;

/**
 * Contains information about a version conflict that occurred during a conditional write.
 *
 * <p>When a MetadataChangeProposal includes an "If-Version-Match" header and the expected version
 * doesn't match the actual version in the database, the server returns a 422 validation error. This
 * class captures the relevant information to enable retry logic.
 */
@Value
public class VersionConflictInfo {
  /** The version that was expected (from the If-Version-Match header). */
  @Nonnull String expectedVersion;

  /** The actual version that exists in the database. */
  @Nonnull String actualVersion;

  /** The MCP that failed due to version mismatch (optional). */
  @Nullable MetadataChangeProposal failedMcp;

  /** The full error message from the server. */
  @Nonnull String errorMessage;
}
