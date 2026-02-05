/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

package com.linkedin.metadata.aspect.patch.template.container;

import com.fasterxml.jackson.databind.JsonNode;
import com.linkedin.container.EditableContainerProperties;
import com.linkedin.data.template.RecordTemplate;
import com.linkedin.metadata.aspect.patch.template.Template;
import javax.annotation.Nonnull;

public class EditableContainerPropertiesTemplate implements Template<EditableContainerProperties> {

  @Override
  public EditableContainerProperties getSubtype(RecordTemplate recordTemplate)
      throws ClassCastException {
    if (recordTemplate instanceof EditableContainerProperties) {
      return (EditableContainerProperties) recordTemplate;
    }
    throw new ClassCastException("Unable to cast RecordTemplate to EditableContainerProperties");
  }

  @Override
  public Class<EditableContainerProperties> getTemplateType() {
    return EditableContainerProperties.class;
  }

  @Nonnull
  @Override
  public EditableContainerProperties getDefault() {
    return new EditableContainerProperties();
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
