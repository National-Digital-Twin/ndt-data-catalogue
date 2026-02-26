/*
 * SPDX-License-Identifier: Apache-2.0
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
package com.linkedin.metadata.config.search;

import org.testng.Assert;
import org.testng.annotations.Test;

public class EmbeddingProviderConfigurationTest {

  @Test
  public void testGetModelId_BedrockReturnsBedrockModel() {
    EmbeddingProviderConfiguration config = new EmbeddingProviderConfiguration();
    config.setType("aws-bedrock");
    config.getBedrock().setModel("cohere.embed-multilingual-v3");

    Assert.assertEquals(config.getModelId(), "cohere.embed-multilingual-v3");
  }

  @Test
  public void testGetModelId_OpenAiReturnsOpenAiModel() {
    EmbeddingProviderConfiguration config = new EmbeddingProviderConfiguration();
    config.setType("openai");
    config.getOpenai().setModel("text-embedding-3-small");

    Assert.assertEquals(config.getModelId(), "text-embedding-3-small");
  }

  @Test
  public void testGetModelId_CohereReturnsCohereModel() {
    EmbeddingProviderConfiguration config = new EmbeddingProviderConfiguration();
    config.setType("cohere");
    config.getCohere().setModel("embed-multilingual-v3.0");

    Assert.assertEquals(config.getModelId(), "embed-multilingual-v3.0");
  }

  @Test
  public void testGetModelId_TypeCaseInsensitive() {
    EmbeddingProviderConfiguration config = new EmbeddingProviderConfiguration();
    config.setType("AWS-BEDROCK");
    config.getBedrock().setModel("amazon.titan-embed-text-v1");

    Assert.assertEquals(config.getModelId(), "amazon.titan-embed-text-v1");
  }

  @Test
  public void testGetModelId_NullTypeReturnsNull() {
    EmbeddingProviderConfiguration config = new EmbeddingProviderConfiguration();
    config.setType(null);

    Assert.assertNull(config.getModelId());
  }

  @Test
  public void testGetModelId_UnknownTypeReturnsNull() {
    EmbeddingProviderConfiguration config = new EmbeddingProviderConfiguration();
    config.setType("unknown-provider");

    Assert.assertNull(config.getModelId());
  }
}
