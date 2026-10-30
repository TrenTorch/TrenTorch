// O(log n) time, O(1) space
function happyNumber(n) {
  function step(x) {
    let total = 0;
    while (x > 0) {
      const digit = x % 10;
      total += digit * digit;
      x = Math.floor(x / 10);
    }
    return total;
  }

  let slow = n;
  let fast = step(n);
  while (fast !== 1 && slow !== fast) {
    slow = step(slow);
    fast = step(step(fast));
  }
  return fast === 1;
}

console.log(happyNumber(19));
