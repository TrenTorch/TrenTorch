// O(n + m) time, O(n + m) space
// Write mergeSortedPair as the problem statement describes.
function mergeSortedPair(a, b) {
  const merged = [];
  let i = 0, j = 0, comparisons = 0;
  const lenA = a.length, lenB = b.length;
  while (i < lenA && j < lenB) {
    comparisons++;
    if (a[i] <= b[j]) {
      merged.push(a[i]);
      i++;
    } else {
      merged.push(b[j]);
      j++;
    }
  }
  while (i < lenA) {
    merged.push(a[i++]);
  }
  while (j < lenB) {
    merged.push(b[j++]);
  }
  return [merged, comparisons];
}
