const fs = require('fs')
const { derive, publickeys, scan } = require('@dotenvx/primitives')

const Errors = require('../helpers/errors')
const upsertEnvKey = require('../helpers/upsertEnvKey')

function latestValues (parsed) {
  const result = {}

  for (const [key, values] of Object.entries(parsed)) {
    result[key] = values[values.length - 1]
  }

  return result
}

function privateKeyring (keysSrc) {
  const { parsed } = scan(keysSrc)
  const values = latestValues(parsed)
  const keyring = {}

  for (const [privateKeyName, privateKey] of Object.entries(values)) {
    if (!privateKeyName.startsWith('DOTENV_PRIVATE_KEY')) continue

    try {
      const publicKey = derive(privateKey)
      keyring[publicKey] = { privateKeyName, privateKeyValue: privateKey }
    } catch {}
  }

  return keyring
}

function lockedKeyring (keysSrc) {
  const { parsed } = scan(keysSrc)
  const values = latestValues(parsed)
  const keyring = {}

  for (const [privateKeyName, privateKey] of Object.entries(values)) {
    if (!privateKeyName.startsWith('DOTENV_PRIVATE_KEY')) continue
    if (!privateKey.startsWith('locked:')) continue

    const parts = privateKey.split(':')
    if (parts.length < 3) continue

    const publicKey = parts[1]
    keyring[publicKey] = {
      privateKeyName,
      lockedPrivateKeyValue: privateKey,
      publicKeyValue: publicKey
    }
  }

  return keyring
}

class LockUp {
  constructor (envFile = '.env', envKeysFile = '.env.keys') {
    this.envFile = envFile
    this.envKeysFile = envKeysFile
  }

  plan () {
    const envFile = this.envFile
    const envKeysFile = this.envKeysFile

    const envSrc = fs.readFileSync(envFile, 'utf8')
    const keysSrc = fs.readFileSync(envKeysFile, 'utf8')
    const ring = privateKeyring(keysSrc)
    const lockedRing = lockedKeyring(keysSrc)
    const matches = []
    const alreadyLocked = []

    for (const publicKey of publickeys(envSrc)) {
      const privateKey = ring[publicKey]
      if (privateKey) {
        matches.push({
          privateKeyName: privateKey.privateKeyName,
          privateKeyValue: privateKey.privateKeyValue,
          publicKeyValue: publicKey
        })
        continue
      }

      const lockedPrivateKey = lockedRing[publicKey]
      if (lockedPrivateKey) {
        alreadyLocked.push(lockedPrivateKey)
      }
    }

    if (matches.length < 1 && alreadyLocked.length < 1) {
      throw new Errors({ key: 'DOTENV_PRIVATE_KEY' }).missingKey()
    }

    return { matches, alreadyLocked }
  }

  matches () {
    const { matches } = this.plan()

    if (matches.length < 1) {
      throw new Errors({ key: 'DOTENV_PRIVATE_KEY' }).missingKey()
    }

    return matches
  }

  run (lockPrivateKey) {
    if (!lockPrivateKey) {
      throw new Error('missing lock private key function')
    }

    const envKeysFile = this.envKeysFile
    const results = []

    const { matches, alreadyLocked } = this.plan()

    for (const privateKey of matches) {
      const lockedPrivateKey = lockPrivateKey(privateKey.privateKeyValue, privateKey.publicKeyValue)
      const result = upsertEnvKey(privateKey.privateKeyName, lockedPrivateKey, envKeysFile)

      results.push({
        changed: result.changed,
        privateKeyName: privateKey.privateKeyName,
        privateKeyValue: privateKey.privateKeyValue,
        lockedPrivateKeyValue: lockedPrivateKey,
        publicKeyValue: privateKey.publicKeyValue
      })
    }

    for (const lockedPrivateKey of alreadyLocked) {
      results.push({
        changed: false,
        privateKeyName: lockedPrivateKey.privateKeyName,
        privateKeyValue: undefined,
        lockedPrivateKeyValue: lockedPrivateKey.lockedPrivateKeyValue,
        publicKeyValue: lockedPrivateKey.publicKeyValue,
        alreadyLocked: true
      })
    }

    return {
      changed: results.some(result => result.changed),
      results
    }
  }
}

module.exports = LockUp
module.exports.privateKeyring = privateKeyring
