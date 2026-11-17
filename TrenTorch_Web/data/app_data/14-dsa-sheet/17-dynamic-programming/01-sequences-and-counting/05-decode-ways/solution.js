// O(n) time, O(1) space
function numDecodings(s) {
  const mod = 1000000007;
  if (s.length === 0) return 0;
  let a = 1, b = 1;
  for (let i = 1; i <= s.length; i++) {
    let now = 0;
    if (s[i - 1] !== '0') {
      now = (now + b) % mod;
    }
    if (i >= 2) {
      const two = s.slice(i - 2, i);
      if (two >= "10" && two <= "26") {
        now = (now + a) % mod;
      }
    }
    a = b;
    b = now;
  }
  return b % mod;
}

console.log(numDecodings("12"));
