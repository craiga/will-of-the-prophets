describe("Rolling", () => {
  it("Logging in and rolling", () => {
    cy.visit("/roll");
    cy.contains("Username").click().type("rollinguser");
    cy.contains("Password").click().type("rolling user password");
    cy.contains("Log In").click();
    cy.get("input[name='embargo']").type("2050-12-31T00:00");
    cy.get("button[type='submit']").click();
    cy.contains("Board as of Dec. 31, 2050");
  });
});
