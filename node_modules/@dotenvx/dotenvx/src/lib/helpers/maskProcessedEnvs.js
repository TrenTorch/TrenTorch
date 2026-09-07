const mask = require('./mask')

function maskProcessedEnvs (processedEnvs, processEnv, showChar) {
  // Track every key resolved from the requested env sources so the same keys
  // can also be masked in the environment receiving the resolved values.
  const resolvedKeys = new Set()

  for (const processedEnv of processedEnvs) {
    for (const key of Object.keys(processedEnv.parsed || {})) {
      resolvedKeys.add(key)
    }

    // These values may be logged, so mask each resolver reporting bucket.
    for (const values of [processedEnv.parsed, processedEnv.injected, processedEnv.existed]) {
      for (const key of Object.keys(values || {})) {
        values[key] = mask(values[key], showChar)
      }
    }
  }

  // Leave unrelated inherited environment variables unchanged.
  for (const key of resolvedKeys) {
    if (processEnv[key] !== undefined) {
      processEnv[key] = mask(processEnv[key], showChar)
    }
  }
}

module.exports = maskProcessedEnvs
