// O(n log n) time, O(n) space
function groupAnagrams(words) {
  const map = new Map();
  for (const word of words) {
    const key = word.split('').sort().join('');
    if (!map.has(key)) {
      map.set(key, []);
    }
    map.get(key).push(word);
  }
  const groups = Array.from(map.values());
  for (const group of groups) {
    group.sort();
  }
  groups.sort((a, b) => {
    if (a[0] < b[0]) return -1;
    if (a[0] > b[0]) return 1;
    return 0;
  });
  return groups;
}

console.log(groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"]));
