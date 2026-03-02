/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

describe("analytics", () => {
  // Skipped: requires the datahub analytics plugin to be enabled (src/conf/analytics.ts datahub.enabled=true)
  // so that EntitySectionViewEvent data is stored in Elasticsearch and shown in the Analytics page.
  // Re-enable once analytics tracking is restored.
  it.skip("can go to a chart and see analytics in tab views", () => {
    cy.login();

    cy.goToChart("urn:li:chart:(looker,cypress_baz1)");
    cy.waitTextVisible("Baz Chart 1");
    cy.openEntityTab("Dashboards");
    cy.wait(1000);

    cy.goToAnalytics();
    cy.contains("Tab Views By Entity Type (Past Week)").scrollIntoView({
      ensureScrollable: false,
    });
    cy.waitTextPresent("dashboards");
  });
});
