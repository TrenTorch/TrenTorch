// O(n) time, O(1) space
function maxProfitCooldown(prices) {
    let hold = -Infinity;
    let sold = 0;
    let rest = 0;
    for (const price of prices) {
        const prevHold = hold;
        const prevSold = sold;
        const prevRest = rest;
        hold = Math.max(prevHold, prevRest - price);
        sold = prevHold + price;
        rest = Math.max(prevRest, prevSold);
    }
    return Math.max(sold, rest);
}

console.log(maxProfitCooldown([1, 2, 3, 0, 2]));
