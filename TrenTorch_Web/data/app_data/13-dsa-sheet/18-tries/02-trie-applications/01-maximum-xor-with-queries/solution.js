// O((N+Q)*30) time, O(N*30) space
function maxXorQueries(nums, queries) {
    const root = [null, null];
    for (const n of nums) {
        let node = root;
        for (let b = 29; b >= 0; b--) {
            const bit = (n >> b) & 1;
            if (!node[bit]) {
                node[bit] = [null, null];
            }
            node = node[bit];
        }
    }
    const out = [];
    for (const x of queries) {
        let node = root;
        let best = 0;
        for (let b = 29; b >= 0; b--) {
            const bit = (x >> b) & 1;
            const desired = 1 - bit;
            if (node[desired]) {
                best |= (1 << b);
                node = node[desired];
            } else {
                node = node[bit];
            }
        }
        out.push(best);
    }
    return out;
}

console.log(maxXorQueries([0, 1, 2, 3, 4], [3, 5]));
