// support/utility-functions/redcap_dom.js

export function visitLoginPage() {
    cy.visit('/', { timeout: 60000 }); // Adjust URL and timeout if needed
}

export function enterUsername(username) {
    cy.get('#username', { timeout: 60000 }).type(username);
}

export function enterPassword(password) {
    cy.get('#password', { timeout: 60000 }).type(password);
}

export function clickLoginButton() {
    cy.get('#login_btn', { timeout: 60000 }).click();
}

export function checkUrlForDashboard() {
    cy.url({ timeout: 60000 }).should('include', 'action=myprojects');
}

export function checkWelcomeMessage() {
    cy.contains('My Projects', { timeout: 60000 }).should('be.visible');
}
