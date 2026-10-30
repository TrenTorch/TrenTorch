// O(n) time, O(1) extra space
function majorityElementThirds(nums) {
  let a = null, b = null;
  let ca = 0, cb = 0;
  for (const x of nums) {
    if (x === a) {
      ca++;
    } else if (x === b) {
      cb++;
    } else if (ca === 0) {
      a = x;
      ca = 1;
    } else if (cb === 0) {
      b = x;
      cb = 1;
    } else {
      ca--;
      cb--;
    }
  }

  const n = nums.length;
  let countA = 0, countB = 0;
  for (const x of nums) {
    if (x === a) countA++;
    else if (x === b) countB++;
  }

  const res = [];
  if (a !== null && countA * 3 > n) res.push(a);
  if (b !== null && b !== a && countB * 3 > n) res.push(b);
  res.sort((x, y) => x - y);
  return res;
}

console.log(majorityElementThirds([3, 2, 3]));
