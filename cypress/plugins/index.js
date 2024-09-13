const cucumber = require('@badeball/cypress-cucumber-preprocessor').default
const browserify = require('@badeball/cypress-cucumber-preprocessor/browserify').default

module.exports = (on, config) => {
    on('file:preprocessor', browserify(config))
    return config
}
