const Session = require('../../../db/session')

function status () {
  console.log(new Session().status())
}

module.exports = status
