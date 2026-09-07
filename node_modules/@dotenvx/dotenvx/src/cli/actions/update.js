const childProcess = require('child_process')

const INSTALL_COMMAND = 'curl -sfS https://dotenvx.sh | sh'

function update () {
  if (process.pkg) {
    childProcess.execSync(INSTALL_COMMAND, { stdio: 'inherit' })
    return
  }

  console.log('global: npm install -g @dotenvx/dotenvx@latest')
  console.log('local:  npm install @dotenvx/dotenvx@latest --save')
}

module.exports = update
