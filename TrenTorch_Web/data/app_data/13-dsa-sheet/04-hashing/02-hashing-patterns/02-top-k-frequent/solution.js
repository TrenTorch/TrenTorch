// O(n) average time, O(n) space
function topKFrequent(nums, k) {
    const freq = new Map();
    for (const num of nums) {
        freq.set(num, (freq.get(num) || 0) + 1);
    }

    const pairs = [];
    for (const [value, count] of freq) {
        pairs.push([-count, value]);
    }

    if (k <= 0) return [];
    if (k >= pairs.length) {
        pairs.sort((a, b) => a[0] - b[0] || a[1] - b[1]);
        return pairs.map(p => p[1]);
    }

    const compare = (a, b) => a[0] - b[0] || a[1] - b[1];

    let need = k;
    let pool = pairs;
    const chosen = [];

    while (need > 0) {
        const pivot = pool[Math.floor(Math.random() * pool.length)];
        const less = [];
        const greater = [];

        for (const p of pool) {
            const c = compare(p, pivot);
            if (c < 0) less.push(p);
            else if (c > 0) greater.push(p);
        }

        if (need <= less.length) {
            pool = less;
        } else if (need === less.length + 1) {
            chosen.push(...less, pivot);
            need = 0;
        } else {
            chosen.push(...less, pivot);
            need -= less.length + 1;
            pool = greater;
        }
    }

    chosen.sort(compare);
    return chosen.map(p => p[1]);
}

console.log(topKFrequent([1, 1, 1, 2, 2, 3], 2));
