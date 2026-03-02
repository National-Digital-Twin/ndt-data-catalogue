/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

package com.linkedin.metadata.aspect.patch.template.ml;

import com.fasterxml.jackson.databind.JsonNode;
import com.linkedin.data.template.RecordTemplate;
import com.linkedin.metadata.aspect.patch.template.Template;
import com.linkedin.ml.metadata.EditableMLModelGroupProperties;
import javax.annotation.Nonnull;

public class EditableMLModelGroupPropertiesTemplate
    implements Template<EditableMLModelGroupProperties> {

  @Override
  public EditableMLModelGroupProperties getSubtype(RecordTemplate recordTemplate)
      throws ClassCastException {
    if (recordTemplate instanceof EditableMLModelGroupProperties) {
      return (EditableMLModelGroupProperties) recordTemplate;
    }
    throw new ClassCastException("Unable to cast RecordTemplate to EditableMLModelGroupProperties");
  }

  @Override
  public Class<EditableMLModelGroupProperties> getTemplateType() {
    return EditableMLModelGroupProperties.class;
  }

  @Nonnull
  @Override
  public EditableMLModelGroupProperties getDefault() {
    return new EditableMLModelGroupProperties();
  }

  @Nonnull
  @Override
  public JsonNode transformFields(JsonNode baseNode) {
    return baseNode;
  }

  @Nonnull
  @Override
  public JsonNode rebaseFields(JsonNode patched) {
    return patched;
  }
}
