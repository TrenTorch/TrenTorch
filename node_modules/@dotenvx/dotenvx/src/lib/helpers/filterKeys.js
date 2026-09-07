const { match } = require('@dotenvx/primitives')

function filterKeys (parsed, includeKeys, excludeKeys) {
  const include = includeKeys && match(includeKeys)
  const exclude = excludeKeys && match(excludeKeys)

  return Object.fromEntries(Object.entries(parsed).filter(([key]) => {
    if (include && !include(key)) return false
    if (exclude && exclude(key)) return false

    return true
  }))
}

module.exports = filterKeys
