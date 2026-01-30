/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

package com.linkedin.metadata.search.api;

import java.util.Set;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;
import lombok.experimental.Accessors;

@Setter
@Getter
@Accessors(fluent = true)
@EqualsAndHashCode
public class SearchDocFieldFetchConfig {

  public static final Set<String> DEFAULT_FIELDS_TO_FETCH_ON_SCROLL = Set.of("urn");
  public static final Set<String> DEFAULT_FIELDS_TO_FETCH_ON_SEARCH =
      Set.of("urn", "usageCountLast30Days");

  private Set<String> fieldsToFetch = DEFAULT_FIELDS_TO_FETCH_ON_SCROLL;
}
