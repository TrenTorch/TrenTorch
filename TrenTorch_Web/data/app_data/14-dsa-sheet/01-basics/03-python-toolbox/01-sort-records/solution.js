// O(n log n) time, O(n) space
function sortRecords(records) {
  return records
    .slice()
    .sort((a, b) => {
      if (b[1] !== a[1]) return b[1] - a[1]; // higher score first
      if (a[0] < b[0]) return -1;           // alphabetical order
      if (a[0] > b[0]) return 1;
      return 0;
    })
    .map(pair => pair[0]);
}
