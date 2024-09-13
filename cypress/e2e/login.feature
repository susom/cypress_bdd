Feature: User Login

  Scenario: Successful login with valid credentials
    Given the user navigates to the login page
    When the user enters username and password
    And the user clicks the login button
    Then the user should be redirected to the dashboard
    And the user should see a welcome message
