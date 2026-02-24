/*
 * SPDX-License-Identifier: Apache-2.0
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

package com.linkedin.metadata.config;

/**
 * Defines how to handle aspects that exceed the configured size threshold during MCP processing.
 *
 * <p>When validation detects oversized aspects:
 *
 * <ul>
 *   <li><b>DELETE:</b> Properly deletes aspect through EntityService after transaction commits,
 *       handling all side effects (Elasticsearch, graph, consumer hooks)
 *   <li><b>IGNORE:</b> Logs warning, skips write, routes MCP to FailedMetadataChangeProposal topic
 * </ul>
 */
public enum OversizedAspectRemediation {
  /**
   * Properly delete the oversized aspect through EntityService. Ensures all side effects are
   * handled: database deletion, Elasticsearch index updates, graph edge cleanup, consumer hook
   * invocation, and system metadata deletion.
   *
   * <p>Deletion happens after database transaction commits using ThreadLocal collection pattern.
   */
  DELETE("deleted"),

  /**
   * Leave the oversized aspect in database (for pre-patch) or skip the write (for post-patch), log
   * warning, and route MCP to FailedMetadataChangeProposal topic for observability.
   */
  IGNORE("write skipped");

  public final String logLabel;

  OversizedAspectRemediation(String logLabel) {
    this.logLabel = logLabel;
  }
}
