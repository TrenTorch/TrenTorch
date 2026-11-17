// O(n log n) time, O(n) space
function minArrows(points) {
  points.sort((a, b) => a[1] - b[1]);
  let arrows = 0;
  let arrow = null;
  for (const [start, end] of points) {
    if (arrow === null || start > arrow) {
      arrows++;
      arrow = end;
    }
  }
  return arrows;
}

console.log(minArrows([[10, 16], [2, 8], [1, 6], [7, 12]]));
