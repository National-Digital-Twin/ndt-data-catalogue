/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

package io.datahubproject.openapi.operations.consistency.models;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.linkedin.metadata.aspect.consistency.check.CheckResult;
import io.swagger.v3.oas.annotations.media.Schema;
import java.util.List;
import javax.annotation.Nonnull;
import javax.annotation.Nullable;
import lombok.Builder;
import lombok.Data;

/** Result of a consistency check operation. */
@Data
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
@Schema(description = "Result of a consistency check operation")
public class ConsistencyCheckResult {

  /** Creates a ConsistencyCheckResult from a service-layer CheckResult. */
  public static ConsistencyCheckResult from(@Nonnull CheckResult result) {
    return ConsistencyCheckResult.builder()
        .entitiesScanned(result.getEntitiesScanned())
        .issuesFound(result.getIssuesFound())
        .issues(ConsistencyIssue.from(result.getIssues()))
        .scrollId(result.getScrollId())
        .build();
  }

  @Schema(description = "Number of entities scanned in this batch")
  private int entitiesScanned;

  @Schema(description = "Number of issues found")
  private int issuesFound;

  @Schema(description = "List of consistency issues found")
  @Nonnull
  private List<ConsistencyIssue> issues;

  @Schema(
      description =
          "Scroll ID for pagination. Null if no more results. Pass to next request to continue.")
  @Nullable
  private String scrollId;
}
