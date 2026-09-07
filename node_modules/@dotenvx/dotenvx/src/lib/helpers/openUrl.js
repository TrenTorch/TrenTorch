const { open } = require('@dotenvx/tooling')

async function openUrl (url) {
  return await open(url, { wait: false })
}

module.exports = openUrl
