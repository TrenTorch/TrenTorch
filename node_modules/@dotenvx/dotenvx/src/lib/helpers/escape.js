function escape (value) {
  const quote = String.fromCharCode(39)
  return quote + value.replaceAll(quote, quote + '\\' + quote + quote) + quote
}

module.exports = escape
