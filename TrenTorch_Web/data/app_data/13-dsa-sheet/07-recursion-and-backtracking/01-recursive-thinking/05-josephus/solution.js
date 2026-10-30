// O(n) time, O(1) space
function josephus(n, k) {
  let position = 0;
  for (let m = 2; m <= n; m++) {
    position = (position + k) % m;
  }
  return position + 1;
}

console.log(josephus(5, 2));
