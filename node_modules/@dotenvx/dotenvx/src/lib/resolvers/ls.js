const { Fdir } = require('@dotenvx/tooling')
const path = require('path')
const { match } = require('@dotenvx/primitives')

const DEFAULT_EXCLUDED_DIRECTORY_EXTENSIONS = new Set([
  '.app',
  '.key',
  '.numbers',
  '.pages',
  '.photoslibrary'
])

function patternsFor (value) {
  if (!Array.isArray(value)) {
    return [`**/${value}`]
  }

  return value.map(part => `**/${part}`)
}

function excludePatternsFor (value) {
  if (!Array.isArray(value)) {
    return [`**/${value}`]
  }

  return value.map(part => `**/${part}`)
}

function crawler (options = {}) {
  const ignore = ['node_modules/**', '**/node_modules/**', '.git/**', '**/.git/**']
  const cwd = path.resolve(options.directory || './')
  const envFile = options.envFile || ['.env*']
  const excludeEnvFile = options.excludeEnvFile || []
  const excludePatterns = excludePatternsFor(excludeEnvFile)
  let excludes
  if (excludePatterns.length > 0) {
    excludes = ignore.concat(excludePatterns)
  } else {
    excludes = ignore
  }
  const exclude = match(excludes, { dot: true })
  const include = match(patternsFor(envFile), {
    dot: true,
    ignore: excludes
  })
  const onDirectory = options.onDirectory || (() => {})

  return new Fdir()
    .withRelativePaths()
    .exclude((dirname, directory) => {
      if (dirname === 'node_modules' || dirname === '.git') return true
      if (DEFAULT_EXCLUDED_DIRECTORY_EXTENSIONS.has(path.extname(dirname).toLowerCase())) return true

      onDirectory(path.relative(cwd, directory) || '.')
      return false
    })
    .filter((filepath) => !exclude(filepath) && include(filepath))
    .crawl(cwd)
}

async function ls (options = {}) {
  return await crawler(options).withPromise()
}

ls.sync = function (options = {}) {
  return crawler(options).sync()
}

module.exports = ls
