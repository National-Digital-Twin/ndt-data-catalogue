/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

package datahub.client.v2.entity;

/**
 * Controls read semantics for aspect retrieval from cache.
 *
 * <p>This enum is used by {@link AspectCache} to determine whether dirty (locally modified) aspects
 * should be returned during reads.
 */
public enum ReadMode {
  /**
   * Allow reading dirty (locally modified) aspects.
   *
   * <p>This provides read-your-own-writes semantics, where local modifications are immediately
   * visible to subsequent reads before being written to the server.
   *
   * <p>This is the default and recommended mode for most operations.
   */
  ALLOW_DIRTY,

  /**
   * Only read clean aspects fetched from the server.
   *
   * <p>This mode skips dirty aspects and only returns data that matches the current server state.
   * Useful for validation, comparison, or when you explicitly need to see server state regardless
   * of local modifications.
   */
  SERVER_ONLY
}
