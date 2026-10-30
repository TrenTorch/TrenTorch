// O(n) time, O(n) space
function isRotation(s, goal) {
  return s.length === goal.length && (s + s).includes(goal);
}

console.log(isRotation("abcde", "cdeab"));
