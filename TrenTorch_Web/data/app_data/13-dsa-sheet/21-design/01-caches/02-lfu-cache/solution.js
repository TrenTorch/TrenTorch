// O(1) average time per operation, O(capacity) space
function runLfu(capacity, ops) {
  const value = new Map();
  const count = new Map();
  const groups = new Map(); // frequency -> Map(key -> true) maintaining insertion order
  let low = 0;

  function touch(key) {
    const c = count.get(key);
    const oldGroup = groups.get(c);
    oldGroup.delete(key);
    if (oldGroup.size === 0) {
      groups.delete(c);
      if (low === c) {
        low++;
      }
    }
    const newCount = c + 1;
    count.set(key, newCount);
    if (!groups.has(newCount)) {
      groups.set(newCount, new Map());
    }
    groups.get(newCount).set(key, true);
  }

  const out = [];
  for (const op of ops) {
    const parts = op.split(' ');
    const key = parseInt(parts[1], 10);
    if (parts[0] === 'get') {
      if (value.has(key)) {
        touch(key);
        out.push(value.get(key));
      } else {
        out.push(-1);
      }
    } else if (capacity > 0) {
      if (value.has(key)) {
        value.set(key, parseInt(parts[2], 10));
        touch(key);
      } else {
        if (value.size === capacity) {
          const lowestGroup = groups.get(low);
          const oldestKey = lowestGroup.keys().next().value;
          lowestGroup.delete(oldestKey);
          if (lowestGroup.size === 0) {
            groups.delete(low);
          }
          value.delete(oldestKey);
          count.delete(oldestKey);
        }
        value.set(key, parseInt(parts[2], 10));
        count.set(key, 1);
        if (!groups.has(1)) {
          groups.set(1, new Map());
        }
        groups.get(1).set(key, true);
        low = 1;
      }
    }
  }
  return out;
}

console.log(runLfu(2, ["put 1 1", "put 2 2", "get 1", "put 3 3", "get 2", "get 3", "put 4 4", "get 1", "get 3", "get 4"]));
