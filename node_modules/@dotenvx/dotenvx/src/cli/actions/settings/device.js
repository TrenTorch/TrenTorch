const { logger } = require('../../../shared/logger')
const Session = require('../../../db/session')
const mask = require('../../../lib/helpers/mask')

function device () {
  const options = this.opts()

  try {
    const value = new Session().devicePublicKey()
    if (value && value.length > 1) {
      console.log(options.unmask ? value : mask(value, 6))
      return
    }

    logger.error('missing device. Try generating one with [dotenvx armor login].')
    process.exit(1)
  } catch (error) {
    logger.error(error.message)
    process.exit(1)
  }
}

module.exports = device
