/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

package com.linkedin.gms.factory.search.semantic;

import com.linkedin.metadata.search.elasticsearch.index.MappingsBuilder;
import com.linkedin.metadata.search.embedding.EmbeddingProvider;
import com.linkedin.metadata.search.semantic.SemanticEntitySearch;
import com.linkedin.metadata.search.semantic.SemanticEntitySearchService;
import com.linkedin.metadata.utils.elasticsearch.SearchClientShim;
import javax.annotation.Nonnull;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class SemanticEntitySearchServiceFactory {

  @Autowired
  @Qualifier("searchClientShim")
  private SearchClientShim<?> searchClient;

  @Autowired
  @Qualifier("embeddingProvider")
  private EmbeddingProvider embeddingProvider;

  @Bean(name = "semanticEntitySearchService")
  @Nonnull
  protected SemanticEntitySearch getInstance(
      @Qualifier("mappingsBuilder") final MappingsBuilder mappingsBuilder) {
    return new SemanticEntitySearchService(searchClient, embeddingProvider, mappingsBuilder);
  }
}
