/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

package com.linkedin.metadata.search;

/**
 * Thrown when a request asks for SEMANTIC search mode but semantic search is disabled for the
 * current environment.
 */
public final class SemanticSearchDisabledException extends RuntimeException {
  public SemanticSearchDisabledException() {
    super("Semantic search is disabled in this environment");
  }
}
