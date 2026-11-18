// O(n) time, O(capacity) space
function runLru(capacity, ops) {
  const cache = new Map();
  const out = [];
  for (const op of ops) {
    const parts = op.split(' ');
    if (parts[0] === 'get') {
      const key = Number(parts[1]);
      if (cache.has(key)) {
        const value = cache.get(key);
        cache.delete(key);
        cache.set(key, value);
        out.push(value);
      } else {
        out.push(-1);
      }
    } else if (capacity > 0) { // put operation
      const key = Number(parts[1]);
      const value = Number(parts[2]);
      if (cache.has(key)) {
        cache.delete(key);
      } else if (cache.size === capacity) {
        const lruKey = cache.keys().next().value;
        cache.delete(lruKey);
      }
      cache.set(key, value);
    }
  }
  return out;
}

console.log(runLru(2, ["put 1 1", "put 2 2", "get 1", "put 3 3", "get 2", "put 4 4", "get 1", "get 3", "get 4"]));
