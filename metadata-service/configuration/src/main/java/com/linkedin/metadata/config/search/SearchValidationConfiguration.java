/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

package com.linkedin.metadata.config.search;

import lombok.Data;

@Data
public class SearchValidationConfiguration {
  private int maxQueryLength = 500;
  private String regex =
      ".*[\\x00-\\x08\\x0B\\x0C\\x0E-\\x1F\\x7F]+.*|(?i).*\\b(java|javax)\\.(util|lang|io|naming|xml|security|beans|management|script|sql)\\.(\\w+\\.)*\\w+.*|(?i).*\\b(org\\.(springframework|apache|hibernate|jboss|codehaus|eclipse)|com\\.sun)\\.(\\w+\\.)*\\w+.*|(?i).*(ldap://|rmi://|dns://|iiop://|corba:|jndi:|oastify\\.com).*|.*(\\u00ac\\u00ed|\\\\xac\\\\xed).*";
  private boolean enabled = true;
  private boolean maxLengthEnabled = true;
}
