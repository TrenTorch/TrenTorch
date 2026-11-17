// O(k * E) time, O(n) space where E is number of flights
function cheapestPrice(n, flights, src, dst, k) {
  const INF = Infinity;
  let best = new Array(n).fill(INF);
  best[src] = 0;
  for (let i = 0; i <= k; i++) {
    const nxt = best.slice();
    for (const [a, b, price] of flights) {
      if (best[a] + price < nxt[b]) {
        nxt[b] = best[a] + price;
      }
    }
    best = nxt;
  }
  return best[dst] === INF ? -1 : best[dst];
}

console.log(cheapestPrice(4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1));
