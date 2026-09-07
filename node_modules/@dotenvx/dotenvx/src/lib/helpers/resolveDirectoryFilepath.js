const fs = require('fs')
const path = require('path')

function resolveDirectoryFilepath (filepath, filename) {
  try {
    if (fs.statSync(filepath).isDirectory()) {
      return path.join(filepath, filename)
    }
  } catch (_error) {
    // Preserve missing paths so the existing error handling can report them.
  }

  return filepath
}

module.exports = resolveDirectoryFilepath
