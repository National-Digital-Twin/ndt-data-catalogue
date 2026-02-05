/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

package com.linkedin.metadata.config.search;

import java.util.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/** Configuration for semantic search indices using k-NN vector similarity. */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class SemanticSearchConfiguration {

  /** Whether semantic search indices should be created. Defaults to false. */
  private boolean enabled;

  /**
   * Set of entity names for which semantic search indices should be created. For example:
   * ["dataset", "chart"].
   */
  private Set<String> enabledEntities;

  /** Map of embedding model configurations keyed by model name. */
  private Map<String, ModelEmbeddingConfig> models;

  /** Configuration for the embedding provider used to generate query embeddings. */
  private EmbeddingProviderConfiguration embeddingProvider;
}
