// O(n log n) time, O(n) space
function minPlatforms(arrivals, departures) {
  const arr = arrivals.slice().sort((a, b) => a - b);
  const dep = departures.slice().sort((a, b) => a - b);
  let current = 0, best = 0;
  let i = 0, j = 0;
  while (i < arr.length) {
    if (arr[i] <= dep[j]) {
      current++;
      if (current > best) best = current;
      i++;
    } else {
      current--;
      j++;
    }
  }
  return best;
}

console.log(minPlatforms([900, 940, 950, 1100, 1500, 1800], [910, 1200, 1120, 1130, 1900, 2000]));
