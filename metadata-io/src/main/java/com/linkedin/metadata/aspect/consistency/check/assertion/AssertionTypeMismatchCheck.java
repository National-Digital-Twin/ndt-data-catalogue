/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

package com.linkedin.metadata.aspect.consistency.check.assertion;

import static com.linkedin.metadata.aspect.utils.AssertionUtils.ASSERTION_TYPE_SUB_PROPERTY_CHECKS;
import static com.linkedin.metadata.aspect.utils.AssertionUtils.getExpectedPropertyName;

import com.linkedin.assertion.AssertionInfo;
import com.linkedin.assertion.AssertionType;
import com.linkedin.common.urn.Urn;
import com.linkedin.entity.EntityResponse;
import com.linkedin.metadata.aspect.consistency.ConsistencyIssue;
import com.linkedin.metadata.aspect.consistency.check.CheckContext;
import com.linkedin.metadata.aspect.consistency.fix.ConsistencyFixType;
import com.linkedin.metadata.models.registry.EntityRegistry;
import java.util.Collections;
import java.util.List;
import java.util.function.Function;
import javax.annotation.Nonnull;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

/**
 * Check that assertions have the correct sub-property populated based on their type.
 *
 * <p>Each assertion type requires a corresponding sub-property to be populated:
 *
 * <ul>
 *   <li>DATASET -&gt; datasetAssertion
 *   <li>FRESHNESS -&gt; freshnessAssertion
 *   <li>VOLUME -&gt; volumeAssertion
 *   <li>SQL -&gt; sqlAssertion
 *   <li>FIELD -&gt; fieldAssertion
 *   <li>DATA_SCHEMA -&gt; schemaAssertion
 *   <li>CUSTOM -&gt; customAssertion
 * </ul>
 *
 * <p>If the type is set but the corresponding sub-property is null or empty, this indicates data
 * corruption and the assertion should be hard-deleted as it cannot be fixed.
 */
@Slf4j
@Component("consistencyAssertionTypeMismatchCheck")
public class AssertionTypeMismatchCheck extends AbstractAssertionCheck {

  public AssertionTypeMismatchCheck(@Nonnull EntityRegistry entityRegistry) {
    super(entityRegistry);
  }

  @Override
  @Nonnull
  public String getName() {
    return "Assertion Type Mismatch";
  }

  @Override
  @Nonnull
  public String getDescription() {
    return "Checks that assertions have the correct sub-property populated based on their type";
  }

  @Override
  @Nonnull
  protected List<ConsistencyIssue> checkAssertion(
      @Nonnull CheckContext ctx,
      @Nonnull Urn assertionUrn,
      @Nonnull EntityResponse response,
      @Nonnull AssertionInfo assertionInfo) {

    // Skip if no type is set
    if (!assertionInfo.hasType()) {
      return Collections.emptyList();
    }

    AssertionType type = assertionInfo.getType();
    Function<AssertionInfo, Boolean> checker = ASSERTION_TYPE_SUB_PROPERTY_CHECKS.get(type);

    // Skip if we don't have a checker for this type (shouldn't happen with known types)
    if (checker == null) {
      log.warn(
          "No type checker configured for assertion type {} on assertion {}", type, assertionUrn);
      return Collections.emptyList();
    }

    // Check if the corresponding sub-property is valid (present and non-empty)
    if (!checker.apply(assertionInfo)) {
      String expectedProperty = getExpectedPropertyName(type);
      return List.of(
          createIssueBuilder(assertionUrn, ConsistencyFixType.HARD_DELETE)
              .description(
                  String.format(
                      "Assertion has type '%s' but %s is null or empty", type, expectedProperty))
              .hardDeleteUrns(List.of(assertionUrn))
              .build());
    }

    return Collections.emptyList();
  }
}
