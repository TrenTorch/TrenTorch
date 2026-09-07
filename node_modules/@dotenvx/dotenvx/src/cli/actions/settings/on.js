const { logger } = require('../../../shared/logger')
const Session = require('../../../db/session')

function on () {
  try {
    new Session().turnOn()
    logger.success('✔ armor: on')
  } catch (error) {
    logger.error(error.message)
    process.exit(1)
  }
}

module.exports = on
