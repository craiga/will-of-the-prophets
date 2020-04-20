describe("Rolling", () => {
  it("Logging in and rolling", () => {
    cy.visit("/roll");
    cy.contains("Username").click().type("rollinguser");
    cy.contains("Password").click().type("rolling user password");
    cy.contains("Log In").click();
    cy.contains("Date and time the next move will be public").click();
    cy.get(".xdsoft_year").click();
    cy.get(".xdsoft_year").contains("2050").click();
    cy.get(".xdsoft_month").click();
    cy.get(".xdsoft_month").contains("December").click();
    cy.get(".xdsoft_date").contains("31").click();
    cy.get("button").contains("Roll!").click();
    cy.contains("Board as of Dec. 31, 2050");
  });
});
