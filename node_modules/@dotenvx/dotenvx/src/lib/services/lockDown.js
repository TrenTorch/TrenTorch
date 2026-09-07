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

function lockedCandidates (keysSrc) {
  const { parsed } = scan(keysSrc)
  const values = latestValues(parsed)
  const candidates = []

  for (const [privateKeyName, privateKey] of Object.entries(values)) {
    if (!privateKeyName.startsWith('DOTENV_PRIVATE_KEY')) continue
    if (!privateKey.startsWith('locked:')) continue

    const parts = privateKey.split(':')
    if (parts.length < 3) continue

    candidates.push({
      privateKeyName,
      lockedPrivateKeyValue: privateKey,
      publicKeyValue: parts[1]
    })
  }

  return candidates
}

function privateKeyring (keysSrc) {
  const { parsed } = scan(keysSrc)
  const values = latestValues(parsed)
  const keyring = {}

  for (const [privateKeyName, privateKey] of Object.entries(values)) {
    if (!privateKeyName.startsWith('DOTENV_PRIVATE_KEY')) continue
    if (privateKey.startsWith('locked:')) continue

    try {
      const publicKey = derive(privateKey)
      keyring[publicKey] = { privateKeyName, privateKeyValue: privateKey }
    } catch {}
  }

  return keyring
}

class LockDown {
  constructor (envFile = '.env', envKeysFile = '.env.keys') {
    this.envFile = envFile
    this.envKeysFile = envKeysFile
  }

  lockedCandidates () {
    const keysSrc = fs.readFileSync(this.envKeysFile, 'utf8')
    const candidates = lockedCandidates(keysSrc)

    if (candidates.length < 1) {
      throw new Errors({ key: 'DOTENV_PRIVATE_KEY' }).missingKey()
    }

    return candidates
  }

  plan () {
    const envSrc = fs.readFileSync(this.envFile, 'utf8')
    const keysSrc = fs.readFileSync(this.envKeysFile, 'utf8')
    const publicKeyValues = publickeys(envSrc)
    const lockedByPublicKey = {}
    const plaintextByPublicKey = privateKeyring(keysSrc)
    const locked = []
    const alreadyUnlocked = []

    for (const lockedPrivateKey of lockedCandidates(keysSrc)) {
      lockedByPublicKey[lockedPrivateKey.publicKeyValue] = lockedPrivateKey
    }

    for (const publicKey of publicKeyValues) {
      const lockedPrivateKey = lockedByPublicKey[publicKey]
      if (lockedPrivateKey) {
        locked.push(lockedPrivateKey)
        continue
      }

      const privateKey = plaintextByPublicKey[publicKey]
      if (privateKey) {
        alreadyUnlocked.push({
          changed: false,
          privateKeyName: privateKey.privateKeyName,
          privateKeyValue: privateKey.privateKeyValue,
          lockedPrivateKeyValue: undefined,
          publicKeyValue: publicKey
        })
      }
    }

    if (locked.length < 1 && alreadyUnlocked.length < 1) {
      throw new Errors({ key: 'DOTENV_PRIVATE_KEY' }).missingKey()
    }

    return { locked, alreadyUnlocked }
  }

  run (unlockPrivateKey) {
    const { locked, alreadyUnlocked } = this.plan()
    const results = [...alreadyUnlocked]

    if (locked.length > 0 && !unlockPrivateKey) {
      throw new Error('missing unlock private key function')
    }

    for (const lockedPrivateKey of locked) {
      let privateKeyValue

      try {
        privateKeyValue = unlockPrivateKey(lockedPrivateKey.lockedPrivateKeyValue)
      } catch (error) {
        throw new Errors({ privateKeyName: lockedPrivateKey.privateKeyName }).invalidPassphrase()
      }

      const publicKeyValue = derive(privateKeyValue)

      if (publicKeyValue !== lockedPrivateKey.publicKeyValue) continue

      const result = upsertEnvKey(lockedPrivateKey.privateKeyName, privateKeyValue, this.envKeysFile)

      results.push({
        changed: result.changed,
        privateKeyName: lockedPrivateKey.privateKeyName,
        privateKeyValue,
        lockedPrivateKeyValue: lockedPrivateKey.lockedPrivateKeyValue,
        publicKeyValue
      })
    }

    if (results.length < 1) {
      throw new Errors({ key: 'DOTENV_PRIVATE_KEY' }).missingKey()
    }

    return {
      changed: results.some(result => result.changed),
      results
    }
  }
}

module.exports = LockDown
module.exports.lockedCandidates = lockedCandidates
