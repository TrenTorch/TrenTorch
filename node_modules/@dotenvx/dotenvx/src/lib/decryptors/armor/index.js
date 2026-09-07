const Session = require('../../../db/session')
const PostArmorDecrypt = require('../../api/postArmorDecrypt')

async function index (src, options = {}) {
  const sesh = new Session()

  const hostname = sesh.hostname()
  const token = sesh.token()
  const devicePublicKey = sesh.devicePublicKey()

  return await new PostArmorDecrypt(
    hostname,
    token,
    devicePublicKey,
    options.publicKey,
    src,
    options.grantToken
  ).run()
}

module.exports = index
