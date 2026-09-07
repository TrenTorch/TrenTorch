const crypto = require('crypto')

const { logger } = require('../../../shared/logger')
const LockUp = require('./../../../lib/services/lockUp')
const armoredKeyDisplay = require('../../../lib/helpers/armoredKeyDisplay')
const prompts = require('../../../lib/helpers/prompts')

function lockedValue (privateKey, passphrase, publicKey) {
  const salt = crypto.randomBytes(16)
  const iv = crypto.randomBytes(12)
  const key = crypto.scryptSync(passphrase, salt, 32)
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv)
  const ciphertext = Buffer.concat([
    cipher.update(privateKey, 'utf8'),
    cipher.final()
  ])
  const tag = cipher.getAuthTag()
  const payload = Buffer.concat([
    Buffer.from([1]),
    salt,
    iv,
    tag,
    ciphertext
  ]).toString('base64url')

  return `locked:${publicKey}:${payload}`
}

async function up () {
  const options = this.opts()
  logger.debug(`options: ${JSON.stringify(options)}`)

  try {
    const lockUp = new LockUp(options.envFile, options.envKeysFile)

    const plan = lockUp.plan()
    let results = plan.alreadyLocked.map(lockedPrivateKey => ({
      changed: false,
      privateKeyName: lockedPrivateKey.privateKeyName,
      privateKeyValue: undefined,
      lockedPrivateKeyValue: lockedPrivateKey.lockedPrivateKeyValue,
      publicKeyValue: lockedPrivateKey.publicKeyValue,
      alreadyLocked: true
    }))

    if (plan.matches.length > 0) {
      const passphrase = await prompts.password({
        message: 'passphrase',
        prefix: '⊡',
        separator: '='
      }, {
        input: process.stdin,
        output: process.stderr
      })

      results = lockUp.run((privateKey, publicKey) => lockedValue(privateKey, passphrase, publicKey)).results
    }

    for (const result of results) {
      const keyDisplay = armoredKeyDisplay(result.publicKeyValue) || result.privateKeyName

      if (result.changed) {
        logger.success(`⊡ locked (${keyDisplay})`)
      } else {
        logger.info(`○ no change (${keyDisplay})`)
      }
    }
  } catch (error) {
    if (error.code === 'PROMPT_CANCELLED') {
      process.exit(130)
      return
    }

    logger.error(error.message)
    process.exit(1)
  }
}

module.exports = up
module.exports.lockedValue = lockedValue
