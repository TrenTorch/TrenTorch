// O(n log log n) time, O(n) space
function countPrimes(n) {
  if (n < 3) return 0;
  const sieve = new Uint8Array(n);
  sieve.fill(1);
  sieve[0] = 0;
  sieve[1] = 0;
  const limit = Math.floor(Math.sqrt(n)) + 1;
  for (let i = 2; i < limit; i++) {
    if (sieve[i]) {
      for (let j = i * i; j < n; j += i) {
        sieve[j] = 0;
      }
    }
  }
  let count = 0;
  for (let i = 0; i < n; i++) {
    count += sieve[i];
  }
  return count;
}

console.log(countPrimes(10));
