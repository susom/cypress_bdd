const { Given, When, Then } = require('@badeball/cypress-cucumber-preprocessor');
import { visitLoginPage, enterUsername, enterPassword, clickLoginButton, checkUrlForDashboard, checkWelcomeMessage } from '../support/utility-functions/redcap_dom';

const username = Cypress.env('CYPRESS_USERNAME');
const password = Cypress.env('CYPRESS_PASSWORD');

Given('the user navigates to the login page', () => {
    cy.task("log", {username, password});
    visitLoginPage();
});

When('the user enters username and password', () => {
    enterUsername(username);
    enterPassword(password);
});

When('the user clicks the login button', () => {
    clickLoginButton();
});

Then('the user should be redirected to the dashboard', () => {
    checkUrlForDashboard();
});

Then('the user should see a welcome message', () => {
    checkWelcomeMessage();
});
