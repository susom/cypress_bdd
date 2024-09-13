const { defineConfig } = require('cypress');
const dotenv = require('dotenv');
const path = require('path');
const addCucumberPreprocessorPlugin = require('@badeball/cypress-cucumber-preprocessor').addCucumberPreprocessorPlugin;
const browserify = require('@badeball/cypress-cucumber-preprocessor/browserify').default;

// Load environment variables from .env file
dotenv.config({ path: path.resolve(__dirname, '../.env') });

module.exports = defineConfig({
  e2e: {
    async setupNodeEvents(on, config) {
      await addCucumberPreprocessorPlugin(on, config);

      on('file:preprocessor', browserify(config));

      on('task', {
        log(message) {
          console.log(message);
          return null;
        }
      });

      return config;
    },
    env: {
      CYPRESS_USERNAME: process.env.CYPRESS_USERNAME,
      CYPRESS_PASSWORD: process.env.CYPRESS_PASSWORD,
      CYPRESS_BASE_URL: process.env.CYPRESS_BASE_URL
    },
    baseUrl: process.env.CYPRESS_BASE_URL,
    specPattern: 'e2e/*.feature',
    stepDefinitions: 'e2e/*.js',
    supportFile: false,
    pageLoadTimeout: 60000
  },
});
