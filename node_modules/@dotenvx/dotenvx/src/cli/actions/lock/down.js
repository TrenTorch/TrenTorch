const crypto = require('crypto')

const { logger } = require('../../../shared/logger')
const LockDown = require('./../../../lib/services/lockDown')
const armoredKeyDisplay = require('../../../lib/helpers/armoredKeyDisplay')
const prompts = require('../../../lib/helpers/prompts')

function unlockedValue (lockedPrivateKey, passphrase) {
  const parts = lockedPrivateKey.split(':')
  const payload = Buffer.from(parts.slice(2).join(':'), 'base64url')
  const version = payload.subarray(0, 1)[0]
  const salt = payload.subarray(1, 17)
  const iv = payload.subarray(17, 29)
  const tag = payload.subarray(29, 45)
  const ciphertext = payload.subarray(45)
  const key = crypto.scryptSync(passphrase, salt, 32)
  const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv)

  if (version !== 1) {
    throw new Error('unsupported locked private key version')
  }

  decipher.setAuthTag(tag)

  return Buffer.concat([
    decipher.update(ciphertext),
    decipher.final()
  ]).toString('utf8')
}

async function down () {
  const options = this.opts()
  logger.debug(`options: ${JSON.stringify(options)}`)

  try {
    const lockDown = new LockDown(options.envFile, options.envKeysFile)
    const plan = lockDown.plan()
    let results = plan.alreadyUnlocked

    if (plan.locked.length > 0) {
      const passphrase = await prompts.password({
        message: 'passphrase',
        prefix: '⊡',
        separator: '='
      }, {
        input: process.stdin,
        output: process.stderr
      })

      results = lockDown.run(lockedPrivateKey => unlockedValue(lockedPrivateKey, passphrase)).results
    }

    for (const result of results) {
      const keyDisplay = armoredKeyDisplay(result.publicKeyValue) || result.privateKeyName

      if (result.changed) {
        logger.success(`⊡ unlocked (${keyDisplay})`)
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

module.exports = down
module.exports.unlockedValue = unlockedValue
