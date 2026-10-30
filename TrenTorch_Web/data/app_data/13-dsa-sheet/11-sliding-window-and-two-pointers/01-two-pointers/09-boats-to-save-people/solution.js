// O(n log n) time, O(n) space
function boatsNeeded(people, limit) {
  const a = [...people].sort((x, y) => x - y);
  let light = 0;
  let heavy = a.length - 1;
  let boats = 0;
  while (light <= heavy) {
    if (a[light] + a[heavy] <= limit) {
      light++;
    }
    heavy--;
    boats++;
  }
  return boats;
}

console.log(boatsNeeded([3, 2, 2, 1], 3));
