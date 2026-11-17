// O(n) time, O(n) space
function runBrowserHistory(homepage, ops) {
  const history = [homepage];
  let index = 0;
  const out = [];
  for (const op of ops) {
    const [kind, arg] = op.split(' ');
    if (kind === 'visit') {
      history.length = index + 1;
      history.push(arg);
      index++;
    } else if (kind === 'back') {
      const k = parseInt(arg, 10);
      index = Math.max(0, index - k);
      out.push(history[index]);
    } else { // forward
      const k = parseInt(arg, 10);
      index = Math.min(history.length - 1, index + k);
      out.push(history[index]);
    }
  }
  return out;
}

console.log(runBrowserHistory("a", ["visit b", "visit c", "back 1", "back 5", "forward 1", "visit d", "forward 3"]));
