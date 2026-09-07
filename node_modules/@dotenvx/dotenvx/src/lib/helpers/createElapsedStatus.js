function createElapsedStatus (onStatus, text) {
  if (!onStatus) return () => {}

  let elapsed = 0
  onStatus(text)

  const timer = setInterval(() => {
    elapsed += 1
    onStatus(`${text} (${elapsed}s)`)
  }, 1000)

  if (timer.unref) timer.unref()

  return () => clearInterval(timer)
}

module.exports = createElapsedStatus
