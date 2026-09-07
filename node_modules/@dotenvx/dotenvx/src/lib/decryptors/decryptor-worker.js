const { runAsWorker } = require('@dotenvx/tooling')
const decryptor = require('./armor/index')

runAsWorker(async (src, options) => {
  return decryptor(src, options)
})
