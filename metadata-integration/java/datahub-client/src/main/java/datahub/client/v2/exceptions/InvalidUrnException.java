/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

package datahub.client.v2.exceptions;

import javax.annotation.Nonnull;
import javax.annotation.Nullable;

/**
 * Exception thrown when a URN string has an invalid format.
 *
 * <p>This typically indicates:
 *
 * <ul>
 *   <li>Malformed URN syntax
 *   <li>Invalid characters in URN
 *   <li>Incorrect URN structure
 * </ul>
 *
 * <p><b>Retry strategy:</b> NOT retryable - indicates a client bug or invalid user input that must
 * be fixed.
 *
 * <p>Example invalid URNs:
 *
 * <pre>
 * "not-a-valid-urn"  // Missing urn:li: prefix
 * "urn:li:tag:"      // Missing tag name
 * ""                 // Empty string
 * </pre>
 */
public class InvalidUrnException extends DataHubClientException {

  @Nullable private final String invalidUrn;

  /**
   * Constructs an InvalidUrnException.
   *
   * @param invalidUrn the invalid URN string that was provided
   * @param cause the underlying exception from URN parsing
   */
  public InvalidUrnException(@Nonnull String invalidUrn, @Nullable Throwable cause) {
    super(String.format("Invalid URN: %s", invalidUrn), cause);
    this.invalidUrn = invalidUrn;
  }

  /**
   * Constructs an InvalidUrnException with a custom message.
   *
   * @param message custom error message
   * @param invalidUrn the invalid URN string that was provided
   * @param cause the underlying exception from URN parsing
   */
  public InvalidUrnException(
      @Nonnull String message, @Nonnull String invalidUrn, @Nullable Throwable cause) {
    super(message, cause);
    this.invalidUrn = invalidUrn;
  }

  /**
   * Returns the invalid URN string that caused this exception.
   *
   * @return the invalid URN, or null if not available
   */
  @Nullable
  public String getInvalidUrn() {
    return invalidUrn;
  }

  @Override
  public String toString() {
    if (invalidUrn != null) {
      return super.toString() + " [invalidUrn=" + invalidUrn + "]";
    }
    return super.toString();
  }
}
