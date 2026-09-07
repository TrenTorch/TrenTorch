const path = require('path')
const { which } = require('@dotenvx/tooling')

function shellQuote (value) {
  const escapedQuote = ['\'', '"', '\'', '"', '\''].join('')
  return `'${`${value}`.replace(/'/g, escapedQuote)}'`
}

function ptyCommand (commandArgs, platform = process.platform) {
  if (!['darwin', 'linux'].includes(platform)) return null

  let script
  try {
    script = path.resolve(which.sync('script'))
  } catch (e) {
    return null
  }

  if (platform === 'darwin') {
    return [script, '-q', '/dev/null', ...commandArgs]
  }

  // util-linux script only accepts the child command as a shell string.
  return [script, '-qefc', commandArgs.map(shellQuote).join(' '), '/dev/null']
}

module.exports = ptyCommand
