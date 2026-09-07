function mask (str, showChar = 6) {
  if (!str || str.length < 1) {
    return ''
  }

  const number = Number(showChar)
  showChar = 0
  if (Number.isFinite(number)) {
    showChar = Math.abs(Math.trunc(number))
  }

  let visibleChars = Math.min(showChar, Math.ceil(str.length / 2))
  if (str.length === 1) {
    visibleChars = 0
  }
  const visiblePart = str.slice(0, visibleChars)
  const maskedPart = '*'.repeat(str.length - visibleChars)

  return visiblePart + maskedPart
}

module.exports = mask
