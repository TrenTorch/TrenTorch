const FRAMES = ['◇', '⬖', '◆', '⬗']
const FRAME_INTERVAL_MS = 80
let activeSpinner

async function createSpinner (options = {}) {
  const stream = process.stderr
  const hasCursorControls = typeof stream.cursorTo === 'function' && typeof stream.clearLine === 'function'
  const enabled = Boolean(stream.isTTY && hasCursorControls && options.spinner !== false && !options.quiet && !options.verbose && !options.debug)
  if (!enabled) return null

  const text = options.text || 'thinking'
  const frames = options.frames || FRAMES

  const { default: yoctoSpinner } = await import('yocto-spinner')
  activeSpinner = yoctoSpinner({
    text,
    spinner: {
      frames,
      interval: FRAME_INTERVAL_MS
    },
    stream
  }).start()

  return activeSpinner
}

createSpinner.stop = function () {
  if (activeSpinner) activeSpinner.stop()
  activeSpinner = null
}

createSpinner.pause = function () {
  if (activeSpinner) activeSpinner.stop()
}

createSpinner.resume = function () {
  if (activeSpinner) activeSpinner.start()
}

module.exports = createSpinner
