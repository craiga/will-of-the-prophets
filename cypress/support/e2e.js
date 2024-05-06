before(() => {
  if (Cypress.env("initCommand")) {
    cy.exec(Cypress.env("initCommand"), { failOnNonZeroExit: false }).then(
      (result) => {
        if (result["code"] != 0) {
          throw new Error(
            `Initialization command failed.\n\nstderr:\n${result["stderr"]}`,
          );
        }
      },
    );
  }
});
