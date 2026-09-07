const { runAsWorker } = require('@dotenvx/tooling')
const provider = require('./armor/index')

runAsWorker(async (publicKeyHex) => {
  return provider(publicKeyHex)
})
