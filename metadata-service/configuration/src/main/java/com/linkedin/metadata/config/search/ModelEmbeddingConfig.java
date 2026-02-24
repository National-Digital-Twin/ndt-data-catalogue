/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

package com.linkedin.metadata.config.search;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/** Configuration for a specific embedding model's k-NN vector settings. */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ModelEmbeddingConfig {

  /**
   * Dimensionality of the embedding vectors for this model. Defaults to 3072 (OpenAI
   * text-embedding-3-large).
   */
  private int vectorDimension = 3072;

  /**
   * k-NN engine to use. Options: "faiss", "nmslib", "lucene". Defaults to "faiss" for best
   * performance with large datasets.
   */
  private String knnEngine = "faiss";

  /**
   * Distance metric for vector similarity. Options: "cosinesimil", "l2", "l1", "linf". Defaults to
   * "cosinesimil" which is standard for text embeddings.
   */
  private String spaceType = "cosinesimil";

  /** HNSW ef_construction parameter. Higher values improve index quality but slow down indexing. */
  private int efConstruction = 128;

  /**
   * HNSW m parameter (number of bidirectional links). Higher values improve recall but increase
   * index size.
   */
  private int m = 16;
}
