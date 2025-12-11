/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import * as utils from "./utils";

const TEST_USER_URN = "urn:li:corpuser:jdoe";
const TEST_GLOSSARY_NODE_URN = "urn:li:glossaryNode:CypressNode";
const TEST_GLOSSARY_TERM_NAME = "CypressTerm";

describe("summary tab - glossary node", () => {
  beforeEach(() => {
    utils.setThemeV2AndSummaryTabFlags(true);
    cy.login();
    cy.goToGlossaryNode(TEST_GLOSSARY_NODE_URN);
    utils.goToSummaryTab();
  });

  it("summary tab", () => {
    utils.testPropertiesSection([
      { name: "Created", type: "CREATED" },
      { name: "Owners", type: "OWNERS", dataTestId: `owner-${TEST_USER_URN}` },
    ]);

    utils.ensureAboutSectionIsVisible();

    utils.testTemplateSection([
      {
        type: "hierarchy",
        // FYI: Contents module has different type in add module menu
        addType: "child-hierarchy",
        name: "Contents",
        value: TEST_GLOSSARY_TERM_NAME,
      },
    ]);
  });
});
