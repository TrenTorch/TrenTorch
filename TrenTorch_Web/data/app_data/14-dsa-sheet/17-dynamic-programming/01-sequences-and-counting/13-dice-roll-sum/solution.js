// O(dice * target) time, O(target) space
function diceWays(dice, faces, target) {
  const mod = 1000000007;
  let row = new Array(target + 1).fill(0);
  row[0] = 1;
  for (let i = 0; i < dice; i++) {
    let prefix = new Array(target + 2).fill(0);
    for (let t = 0; t <= target; t++) {
      prefix[t + 1] = (prefix[t] + row[t]) % mod;
    }
    let nxt = new Array(target + 1).fill(0);
    for (let t = 1; t <= target; t++) {
      let left = Math.max(0, t - faces);
      nxt[t] = (prefix[t] - prefix[left] + mod) % mod;
    }
    row = nxt;
  }
  return row[target];
}

console.log(diceWays(2, 6, 7));
