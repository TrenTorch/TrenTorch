// O(2^n) time, O(2^n) space
function towerOfHanoi(n) {
  const moves = [];

  function move(k, source, target, spare) {
    if (k === 0) return;
    move(k - 1, source, spare, target);
    moves.push([source, target]);
    move(k - 1, spare, target, source);
  }

  move(n, 1, 3, 2);
  return moves;
}

console.log(towerOfHanoi(2));
