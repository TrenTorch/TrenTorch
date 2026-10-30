// O(eggs * answer) time, O(eggs) space
function eggDrop(eggs, floors) {
  if (floors === 0 || eggs === 0) {
    return 0;
  }
  const reach = new Array(eggs + 1).fill(0);
  let drops = 0;
  while (reach[eggs] < floors) {
    drops += 1;
    for (let e = eggs; e >= 1; e -= 1) {
      reach[e] = reach[e - 1] + reach[e] + 1;
    }
  }
  return drops;
}

console.log(eggDrop(2, 6));
