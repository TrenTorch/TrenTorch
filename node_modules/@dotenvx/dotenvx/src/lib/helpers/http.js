const { request } = require('@dotenvx/tooling')

async function http (url, opts = {}) {
  return await request(url, opts)
}

module.exports = { http }
