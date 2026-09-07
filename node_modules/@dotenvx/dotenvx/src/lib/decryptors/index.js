const Session = require('./../../db/session')

const armorDecryptor = require('./armor/index')

function syncArmorDecryptor (src, options) {
  const { createSyncFn } = require('@dotenvx/tooling')
  const runDecryptorSync = createSyncFn(require.resolve('./decryptor-worker.js'))
  return runDecryptorSync(src, options)
}

function armorDecryptorForOptions (options) {
  return (src, decryptOptions) => armorDecryptor(src, {
    ...decryptOptions,
    onStatus: options.onStatus,
    token: options.token,
    command: options.command
  })
}

function syncArmorDecryptorForOptions (options) {
  return (src, decryptOptions) => syncArmorDecryptor(src, {
    ...decryptOptions,
    onStatus: options.onStatus,
    token: options.token,
    command: options.command
  })
}

function useArmor (options, noArmor) {
  return options.noArmor !== true && options.armor !== false && !noArmor
}

async function decryptors (options = {}) {
  if (Object.prototype.hasOwnProperty.call(options, 'decryptor')) {
    return options.decryptor
  }

  if (options.noArmor === true || options.armor === false) {
    return null
  }

  const sesh = new Session()
  const noArmor = !options.token && await sesh.noArmor()
  if (!useArmor(options, noArmor)) {
    return null
  }

  return armorDecryptorForOptions(options)
}

decryptors.sync = function decryptorsSync (options = {}) {
  if (Object.prototype.hasOwnProperty.call(options, 'decryptor')) {
    return options.decryptor
  }

  if (options.noArmor === true || options.armor === false) {
    return null
  }

  const sesh = new Session()
  const noArmor = !options.token && sesh.noArmorSync()
  if (!useArmor(options, noArmor)) {
    return null
  }

  return syncArmorDecryptorForOptions(options)
}

module.exports = decryptors
