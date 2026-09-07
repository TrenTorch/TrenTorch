const conventions = require('./conventions')
const resolveDirectoryFilepath = require('./resolveDirectoryFilepath')

function buildCommandEnvs (envs, convention) {
  const resolvedEnvs = []
  let hasDirectory = false

  for (const env of envs) {
    if (env.type !== 'envFile') {
      resolvedEnvs.push(env)
      continue
    }

    const envFilepath = resolveDirectoryFilepath(env.value, '.env')
    if (envFilepath === env.value) {
      resolvedEnvs.push(env)
      continue
    }

    hasDirectory = true
    if (convention) {
      for (const conventionEnv of conventions(convention)) {
        resolvedEnvs.push({
          ...conventionEnv,
          value: resolveDirectoryFilepath(env.value, conventionEnv.value)
        })
      }
    } else {
      resolvedEnvs.push({ ...env, value: envFilepath })
    }
  }

  if (convention && !hasDirectory) {
    return conventions(convention).concat(resolvedEnvs)
  }

  return resolvedEnvs
}

module.exports = buildCommandEnvs
