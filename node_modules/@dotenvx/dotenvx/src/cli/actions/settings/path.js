const { logger } = require('../../../shared/logger')
const Session = require('../../../db/session')

function path () {
  try {
    const value = new Session().path()
    if (value && value.length > 1) {
      console.log(value)
      return
    }

    logger.error('missing path. Try running [dotenvx armor login].')
    process.exit(1)
  } catch (error) {
    logger.error(error.message)
    process.exit(1)
  }
}

module.exports = path
