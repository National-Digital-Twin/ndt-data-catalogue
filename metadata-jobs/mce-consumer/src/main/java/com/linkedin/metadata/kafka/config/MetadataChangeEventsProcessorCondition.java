/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

package com.linkedin.metadata.kafka.config;

import javax.annotation.Nonnull;
import org.springframework.context.annotation.Condition;
import org.springframework.context.annotation.ConditionContext;
import org.springframework.core.env.Environment;
import org.springframework.core.type.AnnotatedTypeMetadata;

/**
 * Condition for enabling the legacy MCE (MetadataChangeEvents) consumer.
 *
 * <p>Enable with: MCE_CONSUMER_ENABLED=true
 */
public class MetadataChangeEventsProcessorCondition implements Condition {
  @Override
  public boolean matches(ConditionContext context, @Nonnull AnnotatedTypeMetadata metadata) {
    Environment env = context.getEnvironment();
    // MCE consumer should be enabled whenever MCE_CONSUMER_ENABLED=true,
    // regardless of batch mode (since there is no batch MCE consumer)
    return "true".equals(env.getProperty("MCE_CONSUMER_ENABLED"));
  }
}
