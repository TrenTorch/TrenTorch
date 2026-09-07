const { WriteStream } = require('tty')

const getColorDepth = (stream) => {
  if (stream && !stream.isTTY) return 1

  try {
    if (stream && typeof stream.getColorDepth === 'function') {
      return stream.getColorDepth()
    }

    return WriteStream.prototype.getColorDepth()
  } catch (error) {
    const term = process.env.TERM

    if (term && (term.includes('256color') || term.includes('xterm'))) {
      return 8 // 256 colors
    }

    return 4
  }
}

module.exports = { getColorDepth }
