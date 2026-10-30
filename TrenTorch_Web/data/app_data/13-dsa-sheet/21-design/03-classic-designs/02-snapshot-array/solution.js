// O(m log k) time, O(m) space where m is number of operations, k is number of snapshots per index
function runSnapshotArray(length, ops) {
  const ids = new Map();
  const vals = new Map();
  let snapId = 0;
  const out = [];
  for (const op of ops) {
    const parts = op.split(' ');
    if (parts[0] === 'set') {
      const i = parseInt(parts[1], 10);
      const v = parseInt(parts[2], 10);
      if (!ids.has(i)) {
        ids.set(i, []);
        vals.set(i, []);
      }
      const idList = ids.get(i);
      const valList = vals.get(i);
      if (idList.length > 0 && idList[idList.length - 1] === snapId) {
        valList[valList.length - 1] = v;
      } else {
        idList.push(snapId);
        valList.push(v);
      }
    } else if (parts[0] === 'snap') {
      out.push(snapId);
      snapId++;
    } else { // get
      const i = parseInt(parts[1], 10);
      const want = parseInt(parts[2], 10);
      const idList = ids.get(i);
      if (!idList || idList.length === 0) {
        out.push(0);
      } else {
        let lo = 0;
        let hi = idList.length;
        while (lo < hi) {
          const mid = (lo + hi) >> 1;
          if (idList[mid] <= want) {
            lo = mid + 1;
          } else {
            hi = mid;
          }
        }
        const k = lo - 1;
        out.push(k >= 0 ? vals.get(i)[k] : 0);
      }
    }
  }
  return out;
}

console.log(runSnapshotArray(3, ["set 0 5", "snap", "set 0 6", "get 0 0", "snap", "get 0 1"]));
