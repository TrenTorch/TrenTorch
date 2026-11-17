// O(n log n) time, O(n) space
function suggestedProducts(products, searchWord) {
  products.sort();
  const out = [];
  for (let i = 1; i <= searchWord.length; i++) {
    const prefix = searchWord.slice(0, i);
    let left = 0;
    let right = products.length;
    while (left < right) {
      const mid = (left + right) >> 1;
      if (products[mid] < prefix) {
        left = mid + 1;
      } else {
        right = mid;
      }
    }
    const suggestions = [];
    for (let j = left; j < Math.min(left + 3, products.length); j++) {
      if (products[j].startsWith(prefix)) {
        suggestions.push(products[j]);
      } else {
        break;
      }
    }
    out.push(suggestions);
  }
  return out;
}

console.log(suggestedProducts(["mobile", "mouse", "moneypot", "monitor", "mousepad"], "mouse"));
