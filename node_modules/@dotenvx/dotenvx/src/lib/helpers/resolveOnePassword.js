const { execFile, execFileSync } = require('child_process')
const Errors = require('./errors')
const createElapsedStatus = require('./createElapsedStatus')

function execFileAsync (command, args, options) {
  return new Promise((resolve, reject) => {
    execFile(command, args, options, (error, stdout) => {
      if (error) return reject(error)
      resolve(stdout)
    })
  })
}

function isSecretReference (value) {
  return typeof value === 'string' && value.startsWith('op://')
}

function resolutionError (key, error) {
  const message = error && error.code === 'ENOENT'
    ? `1Password CLI is not installed and could not resolve ${key}`
    : `1Password CLI failed to resolve ${key}`

  return new Errors({ message }).onePasswordFailed()
}

async function resolveOnePassword (parsed, options = {}) {
  const errors = []
  const unresolved = []
  const hasSecretReferences = Object.values(parsed).some(isSecretReference)
  const stopStatus = hasSecretReferences
    ? createElapsedStatus(options.onStatus, 'awaiting 1password')
    : null

  try {
    for (const [key, value] of Object.entries(parsed)) {
      if (!isSecretReference(value)) continue

      try {
        const stdout = await execFileAsync('op', ['read', value, '--no-newline'], {
          encoding: 'utf8',
          windowsHide: true
        })
        parsed[key] = stdout
      } catch (error) {
        errors.push(resolutionError(key, error))
        unresolved.push(key)
      }
    }
  } finally {
    if (stopStatus) {
      stopStatus()
      if (options.onStatus) options.onStatus('injecting')
    }
  }

  return { errors, unresolved }
}

function resolveOnePasswordSync (parsed) {
  const errors = []
  const unresolved = []

  for (const [key, value] of Object.entries(parsed)) {
    if (!isSecretReference(value)) continue

    try {
      parsed[key] = execFileSync('op', ['read', value, '--no-newline'], {
        encoding: 'utf8',
        windowsHide: true,
        stdio: ['ignore', 'pipe', 'pipe']
      })
    } catch (error) {
      errors.push(resolutionError(key, error))
      unresolved.push(key)
    }
  }

  return { errors, unresolved }
}

module.exports = resolveOnePassword
module.exports.sync = resolveOnePasswordSync
