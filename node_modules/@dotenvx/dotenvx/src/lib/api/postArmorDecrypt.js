const { http } = require('../helpers/http')
const buildApiError = require('../helpers/buildApiError')
const packageJson = require('../helpers/packageJson')
const normalizeToken = require('../helpers/normalizeToken')

class PostArmorDecrypt {
  constructor (hostname, token, devicePublicKey, publicKey, src, grantToken) {
    this.hostname = hostname || 'https://armor.dotenvx.com'
    this.token = token
    this.devicePublicKey = devicePublicKey
    this.publicKey = publicKey
    this.src = src
    this.grantToken = grantToken
  }

  async run () {
    const token = normalizeToken(this.token)
    const url = `${this.hostname}/api/armor/decrypt`
    const body = {
      device_public_key: this.devicePublicKey,
      cli_version: packageJson.version,
      public_key: this.publicKey,
      src: this.src
    }

    if (this.grantToken) {
      body.grant_token = this.grantToken
    }

    const resp = await http(url, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    })

    const json = await resp.body.json()

    if (resp.statusCode >= 400) {
      throw buildApiError(resp.statusCode, json)
    }

    return json
  }
}

module.exports = PostArmorDecrypt
