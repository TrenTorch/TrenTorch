function redact (str) {
  if (!str || str.length < 1) {
    return ''
  }

  return '[REDACTED]'
}

module.exports = redact
