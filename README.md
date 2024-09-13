# Cypress BDD with AI

This project implements BDD (Behavior-Driven Development) testing using Cypress. The setup leverages Docker to create consistent testing environments and integrates AI-driven Python scripts for utility automation, including step definition generation and DOM verification.

## Project Goals

- **BDD Testing**: Use Cypress for end-to-end testing with a behavior-driven approach.
- **Dockerized Setup**: Ensure reproducibility and isolated environments using Docker Compose.
- **AI Integration**: Automate step generation and DOM element verification with Python scripts interacting with AI:
  - Automatically generate step definitions from feature files.
  - Ensure that utility functions (selectors, DOM interactions) remain synchronized with the latest REDCap UI changes.

## Services Overview

The project is orchestrated with Docker Compose and has two main services:

- **ai\_scripts**: Handles AI-driven file generation and DOM consistency checks, ensuring the `redcap_dom.js` utility functions remain aligned with REDCap's structure.
- **cypress**: Executes headless BDD tests and is integrated into the CI/CD pipeline.

Additionally, Cypress can be run locally in an interactive UI mode for test development and debugging.

## Interaction with REDCap

This project is designed to interact with a Dockerized REDCap instance. Ensure the REDCap instance is running and accessible at the `CYPRESS_BASE_URL` before executing Cypress tests. The URL should point to the REDCap instance's address and port.

### Prerequisites

Ensure the following are installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Node.js and npm](https://nodejs.org/) (for local Cypress UI)
- [Python 3](https://www.python.org/) (for running AI scripts)

### Environment Variables

Create a `.env` file in the root directory of your project with the following variables:

```env
CYPRESS_BASE_URL=http://localhost:80
CYPRESS_USERNAME=your-username
CYPRESS_PASSWORD=your-password
GPT_ENDPOINT=https://your-institution-gpt-endpoint
SUBSCRIPTION_KEY=your-subscription-key
```

### Key Features

- **Cypress UI Mode**: For local testing and debugging.
- **Headless Mode**: For CI/CD pipelines, executed via Docker Compose.
- **AI Scripts**: Generate Cypress step definitions and verify utility functions, keeping your test and DOM interactions up to date.


## Gherkin Syntax and Usage

Gherkin is a language used to write feature files for BDD. It is designed to be easy to understand by non-developers, providing a clear syntax for specifying test scenarios.

### Basic Syntax

Gherkin uses several keywords to define features, scenarios, and steps:

- **Feature**: Describes the feature being tested.
- **Scenario**: Represents a specific test case or example.
- **Given**, **When**, **Then**, **And**, **But**: Define steps within a scenario.

### Example

Here’s an example of a Gherkin feature file to test user login functionality with parameterized username and password:

**login.feature**:
```gherkin
Feature: User Login

  Scenario: Successful login with valid credentials
    Given the user navigates to the login page
    When the user enters username "user1" and password "password123"
    And the user clicks the login button
    Then the user should be redirected to the dashboard
    And the user should see the welcome message "Welcome, user1!"
```

### Storing Gherkin Files

In this system, Gherkin feature files are stored in the \`e2e/\` directory. You can create multiple \`.feature\` files for different scenarios and features.

### Transforming Gherkin to Steps

AI scripts are used to transform Gherkin feature files into step definitions needed for Cypress to execute the tests. The \`ai_worker.py\` script is responsible for this transformation.

Here’s an example of what the above Gherkin scenario might transform into:

**login_steps.js**:
```js
const { Given, When, Then } = require('cypress-cucumber-preprocessor/steps');

Given('the user navigates to the login page', () => {
  cy.visit('/login');
});

When('the user enters username {string} and password {string}', (username, password) => {
  cy.get('#username').type(username);
  cy.get('#password').type(password);
});

When('the user clicks the login button', () => {
  cy.get('button[type=submit]').click();
});

Then('the user should be redirected to the dashboard', () => {
  cy.url().should('include', '/dashboard');
});

Then('the user should see the welcome message {string}', (welcomeMessage) => {
  cy.contains(welcomeMessage).should('be.visible');
});
```

## Docker Setup

Build the Docker Containers:

```
docker compose build
```


## Usage

### Running Tests

You have two options for running Cypress tests.

#### 1. Running Tests in Headless Mode (One-Time Execution)

This option runs the tests once in headless mode and automatically shuts down the container when the tests finish. You don't need to start the services separately for this.

To run the tests in headless mode:
``` 
docker compose up cypress 
```


#### 2. Running Tests with Cypress UI (Interactive Mode)

This option opens the Cypress UI, where you can interactively view and debug tests. For this, you need to run the tests locally (outside of Docker) using `npx` after installing the necessary dependencies:

First, ensure you have installed Cypress locally:
``` 
cd /cypress/
npm install 
```
Then, run Cypress in interactive mode:
``` 
npx cypress open
```



### AI Scripts

The 'ai' service is designed for one-time executions to assist in generating the necessary files locally. 
The generated files should then be checked into version control for use in testing.

**update_utilities.sh**: Updates utility functions based on the latest page structure.
``` 
docker compose run --rm ai sh /app/ai_scripts/update_utilities.sh 
```

**regenerate_steps.sh**: Regenerates step definitions from Gherkin feature files.
``` 
docker compose run --rm ai sh /app/ai_scripts/regenerate_steps.sh 
```