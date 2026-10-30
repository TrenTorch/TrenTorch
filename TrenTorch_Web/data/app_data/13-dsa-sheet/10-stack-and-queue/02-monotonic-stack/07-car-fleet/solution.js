// O(n log n) time, O(1) extra space (excluding input)
function carFleet(target, cars) {
  let fleets = 0;
  let slowNum = 0, slowDen = 1;
  cars.sort((a, b) => b[0] - a[0]); // sort by position descending
  for (let i = 0; i < cars.length; i++) {
    const pos = cars[i][0];
    const spd = cars[i][1];
    const num = target - pos;
    const den = spd;
    if (num * slowDen > slowNum * den) {
      fleets++;
      slowNum = num;
      slowDen = den;
    }
  }
  return fleets;
}

console.log(carFleet(12, [[10, 2], [8, 4], [0, 1], [5, 1], [3, 3]]));
