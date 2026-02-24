/*
 * SPDX-License-Identifier: Apache-2.0
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

package datahub.client.v2.entity;

import com.linkedin.common.urn.Urn;
import java.net.URISyntaxException;
import javax.annotation.Nonnull;

/**
 * Helper for structured property URN conversion. Package-private for use by HasStructuredProperties
 * (avoids private interface methods for Java 8 compatibility).
 */
final class StructuredPropertyUrns {

  private StructuredPropertyUrns() {}

  @Nonnull
  static Urn makeStructuredPropertyUrn(@Nonnull String propertyUrn) {
    String fullUrn =
        propertyUrn.startsWith("urn:li:structuredProperty:")
            ? propertyUrn
            : "urn:li:structuredProperty:" + propertyUrn;
    try {
      return Urn.createFromString(fullUrn);
    } catch (URISyntaxException e) {
      throw new datahub.client.v2.exceptions.InvalidUrnException(fullUrn, e);
    }
  }
}
