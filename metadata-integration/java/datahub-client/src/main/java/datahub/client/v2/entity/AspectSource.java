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
 * Indicates the source of a cached aspect.
 *
 * <p>This enum is used by {@link AspectCache} to track whether an aspect was fetched from the
 * server or created/modified locally.
 */
public enum AspectSource {
  /**
   * Aspect was fetched from the DataHub server.
   *
   * <p>SERVER-sourced aspects are subject to TTL expiration.
   */
  SERVER,

  /**
   * Aspect was created or modified locally.
   *
   * <p>LOCAL-sourced aspects do not expire and always represent pending writes.
   */
  LOCAL
}
