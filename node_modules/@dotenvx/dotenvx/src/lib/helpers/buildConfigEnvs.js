const buildCommandEnvs = require('./buildCommandEnvs')
const buildEnvs = require('./buildEnvs')

function buildConfigEnvs (options = {}) {
  if (options.envs) {
    return options.envs
  }

  const pathOptions = { ...options, convention: undefined }
  return buildCommandEnvs(buildEnvs(pathOptions), options.convention)
}

module.exports = buildConfigEnvs
