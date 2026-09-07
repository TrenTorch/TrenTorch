const resolveDirectoryFilepath = require('./resolveDirectoryFilepath')

function resolveEnvKeysFile (envKeysFile) {
  if (Array.isArray(envKeysFile)) {
    return envKeysFile.map(filepath => resolveDirectoryFilepath(filepath, '.env.keys'))
  }

  return envKeysFile && resolveDirectoryFilepath(envKeysFile, '.env.keys')
}

module.exports = resolveEnvKeysFile
