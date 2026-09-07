const { logger } = require('../../../shared/logger')
const Session = require('../../../db/session')

function off () {
  try {
    new Session().turnOff()
    logger.success('✔ armor: off')
  } catch (error) {
    logger.error(error.message)
    process.exit(1)
  }
}

module.exports = off
