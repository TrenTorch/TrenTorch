const keynames = require('../conventions/keynames')
const readEnvKey = require('../helpers/readEnvKey')
const armoredKeyDisplay = require('../helpers/armoredKeyDisplay')
const nativeProvider = require('../providers/native')

class KeychainPush {
  constructor (envFile = '.env', envKeysFile = '.env.keys') {
    this.envFile = envFile
    this.envKeysFile = envKeysFile
  }

  run () {
    const envFile = this.envFile
    const envKeysFile = this.envKeysFile

    const {
      publicKeyName,
      privateKeyName
    } = keynames(envFile)

    const publicKey = readEnvKey(publicKeyName, envFile, { strict: true, ignore: ['MISSING_PRIVATE_KEY'] })
    const privateKey = readEnvKey(privateKeyName, envKeysFile, { strict: true })
    const label = `dotenvx (${armoredKeyDisplay(publicKey)})`

    try {
      const existingPrivateKey = nativeProvider.get(publicKey)

      if (existingPrivateKey === privateKey) {
        return {
          changed: false,
          label,
          privateKeyName,
          privateKeyValue: privateKey,
          publicKeyValue: publicKey
        }
      }
    } catch {}

    nativeProvider.set(publicKey, privateKey, label)

    return {
      changed: true,
      label,
      privateKeyName,
      privateKeyValue: privateKey,
      publicKeyValue: publicKey
    }
  }
}

module.exports = KeychainPush
