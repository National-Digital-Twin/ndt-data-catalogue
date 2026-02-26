/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

describe("login", () => {
  beforeEach(() => {
    cy.setIsThemeV2Enabled(true);
  });

  it("logs in", () => {
    cy.visit("/");
    cy.get("input[data-testid=username]").type(Cypress.env("ADMIN_USERNAME"));
    cy.get("input[data-testid=password]").type(Cypress.env("ADMIN_PASSWORD"));
    // Set localStorage key before navigation so the introduce page is skipped
    // when the app loads after sign-in redirect
    cy.skipIntroducePage();
    cy.get('[data-testid="sign-in"]').click();
    // "Discover" was a V1 nav group title that no longer exists in the V2 nav redesign.
    // Assert on the search input which is always rendered in the V2 header.
    cy.get('[data-testid="search-input"]').should("exist");
  });
});
