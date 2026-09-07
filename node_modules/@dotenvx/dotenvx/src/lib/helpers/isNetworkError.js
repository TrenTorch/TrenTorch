const NETWORK_ERROR_CODES = new Set([
  'ECONNRESET',
  'ECONNREFUSED',
  'ENOTFOUND',
  'ENETDOWN',
  'ENETUNREACH',
  'EHOSTDOWN',
  'EHOSTUNREACH',
  'EPIPE',
  'ETIMEDOUT',
  'UND_ERR_CONNECT_TIMEOUT',
  'UND_ERR_HEADERS_TIMEOUT',
  'UND_ERR_BODY_TIMEOUT',
  'UND_ERR_SOCKET'
])

function isNetworkError (error) {
  return NETWORK_ERROR_CODES.has(error && error.code) || NETWORK_ERROR_CODES.has(error && error.cause && error.cause.code)
}

module.exports = isNetworkError
