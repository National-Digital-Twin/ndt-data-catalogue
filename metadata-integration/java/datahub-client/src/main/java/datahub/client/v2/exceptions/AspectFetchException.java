/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

package datahub.client.v2.exceptions;

import com.linkedin.common.urn.Urn;
import javax.annotation.Nonnull;
import javax.annotation.Nullable;

/**
 * Exception thrown when fetching an aspect from the DataHub server fails.
 *
 * <p>This typically indicates transient failures like:
 *
 * <ul>
 *   <li>Network connectivity issues
 *   <li>Server timeouts or unavailability
 *   <li>HTTP errors (4xx, 5xx)
 *   <li>Authentication/authorization failures
 * </ul>
 *
 * <p><b>Retry strategy:</b> Often retryable for transient network issues, but check the cause to
 * determine if retry is appropriate (e.g., don't retry authentication failures).
 *
 * <p>Note: This is NOT thrown when an aspect doesn't exist for an entity - in that case, the
 * operation returns null.
 */
public class AspectFetchException extends DataHubClientException {

  /**
   * Constructs an AspectFetchException with full context.
   *
   * @param entityUrn the URN of the entity for which aspect fetch failed
   * @param aspectName the name of the aspect that couldn't be fetched
   * @param cause the underlying exception that caused the fetch failure
   */
  public AspectFetchException(
      @Nonnull Urn entityUrn, @Nonnull String aspectName, @Nullable Throwable cause) {
    super(
        String.format("Failed to fetch aspect %s for entity %s", aspectName, entityUrn),
        cause,
        entityUrn,
        aspectName,
        "fetch");
  }

  /**
   * Constructs an AspectFetchException with a custom message.
   *
   * @param message custom error message
   * @param entityUrn the URN of the entity for which aspect fetch failed
   * @param aspectName the name of the aspect that couldn't be fetched
   * @param cause the underlying exception that caused the fetch failure
   */
  public AspectFetchException(
      @Nonnull String message,
      @Nonnull Urn entityUrn,
      @Nonnull String aspectName,
      @Nullable Throwable cause) {
    super(message, cause, entityUrn, aspectName, "fetch");
  }
}
