import argparse
import os
import openai
from pyppeteer import launch
import re
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GPT_ENDPOINT = os.getenv("GPT_ENDPOINT")
SUBSCRIPTION_KEY = os.getenv("SUBSCRIPTION_KEY")

# Initialize the OpenAI client with custom endpoint and subscription key
openai.api_base = GPT_ENDPOINT
openai.api_key = SUBSCRIPTION_KEY

# Function to scrape and update selectors
async def scrape_and_update_selectors():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('http://localhost:8888/login')

    # Scrape a selector
    username_selector = await page.evaluate("() => document.querySelector('input[name=\"username\"]').selectorText")
    password_selector = await page.evaluate("() => document.querySelector('input[name=\"password\"]').selectorText")

    await browser.close()

    # Update Utility.js
    auth_js_path = '/e2e/cypress/support/utility-functions/auth.js'

    with open(auth_js_path, 'w') as file:
        file.write(f"""
        export const login = () => {{
            cy.visit(Cypress.env('baseUrl') + '/login');
            cy.get('{username_selector}').type(Cypress.env('USERNAME'));
            cy.get('{password_selector}').type(Cypress.env('PASSWORD'));
            cy.get('button[type="submit"]').click();
        }};
        """)

# Function to rename functions to be descriptive
def update_function_names():
    auth_js_path = '/e2e/cypress/support/utility-functions/auth.js'

    with open(auth_js_path, 'r') as file:
        content = file.read()

    content = re.sub(r'const login =', 'const userLoginWithValidCredentials =', content)

    with open(auth_js_path, 'w') as file:
        file.write(content)

# Function to generate step definitions from Gherkin
def generate_step_definitions():
    for root, dirs, files in os.walk('/e2e/cypress/integration'):
        for file in files:
            if file.endswith('.feature'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as feature_file:
                    steps = [line.strip() for line in feature_file if line.startswith(('Given', 'When', 'Then', 'And'))]

                step_definitions = ""
                for step in steps:
                    # Use OpenAI to generate step definitions
                    response = openai.Completion.create(
                        engine="davinci-codex",
                        prompt=f"Generate a step definition for '{step}':",
                        max_tokens=150
                    )
                    step_definitions += response.choices[0].text.strip() + "\n"

                with open(filepath.replace('.feature', '_steps.js'), 'w') as step_file:
                    step_file.write(step_definitions)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', required=True, help="Specify the task to run: regenerate-steps, update-utilities")
    args = parser.parse_args()

    if args.task == 'regenerate-steps':
        generate_step_definitions()
    elif args.task == 'update-utilities':
        asyncio.get_event_loop().run_until_complete(scrape_and_update_selectors())
        update_function_names()
    else:
        print(f"Unknown task: {args.task}")

if __name__ == '__main__':
    main()
