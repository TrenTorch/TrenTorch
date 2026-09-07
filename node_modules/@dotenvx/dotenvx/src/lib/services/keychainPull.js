const keynames = require('../conventions/keynames')
const readEnvKey = require('../helpers/readEnvKey')
const upsertEnvKey = require('../helpers/upsertEnvKey')
const armoredKeyDisplay = require('../helpers/armoredKeyDisplay')
const nativeProvider = require('../providers/native')

class KeychainPull {
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
    let privateKey

    try {
      privateKey = nativeProvider.get(publicKey)
      if (!privateKey) throw new Error('not found')
    } catch {
      const secretStore = process.platform === 'win32'
        ? 'Windows Credential Manager'
        : process.platform === 'linux' ? 'Linux Secret Service' : 'macOS Keychain'
      throw new Error(`[NOT_FOUND] private key not found in ${secretStore} (${armoredKeyDisplay(publicKey)}). fix: [dotenvx native up]`)
    }

    const result = upsertEnvKey(privateKeyName, privateKey, envKeysFile)

    return {
      changed: result.changed,
      privateKeyName,
      privateKeyValue: privateKey,
      publicKeyValue: publicKey
    }
  }
}

module.exports = KeychainPull
