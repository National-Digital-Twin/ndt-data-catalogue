/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

package com.linkedin.datahub.upgrade.system.restoreindices.mlmodel;

import static com.linkedin.metadata.Constants.*;

import com.linkedin.datahub.upgrade.system.AbstractMCLStep;
import com.linkedin.metadata.entity.AspectDao;
import com.linkedin.metadata.entity.EntityService;
import io.datahubproject.metadata.context.OperationContext;
import javax.annotation.Nonnull;
import lombok.extern.slf4j.Slf4j;
import org.jetbrains.annotations.Nullable;

@Slf4j
public class ReindexMLModelStep extends AbstractMCLStep {

  public ReindexMLModelStep(
      OperationContext opContext,
      EntityService<?> entityService,
      AspectDao aspectDao,
      Integer batchSize,
      Integer batchDelayMs,
      Integer limit) {
    super(opContext, entityService, aspectDao, batchSize, batchDelayMs, limit);
  }

  @Override
  public String id() {
    return "mlmodel-key-v1";
  }

  @Nonnull
  @Override
  protected String getAspectName() {
    return ML_MODEL_KEY_ASPECT_NAME;
  }

  @Nullable
  @Override
  protected String getUrnLike() {
    return "urn:li:" + ML_MODEL_ENTITY_NAME + ":%";
  }
}
