// O(n α(n)) time, O(n) space
function removeStones(stones) {
    const parent = new Map();
    const size = new Map();

    function find(a) {
        if (!parent.has(a)) {
            parent.set(a, a);
            size.set(a, 1);
        }
        // Path compression (two-pass)
        let root = a;
        while (parent.get(root) !== root) {
            root = parent.get(root);
        }
        let curr = a;
        while (parent.get(curr) !== curr) {
            const next = parent.get(curr);
            parent.set(curr, root);
            curr = next;
        }
        return root;
    }

    for (const [x, y] of stones) {
        let ra = find(x);
        let rb = find(y + 10001);
        if (ra !== rb) {
            // union by size
            if (size.get(ra) < size.get(rb)) {
                const tmp = ra;
                ra = rb;
                rb = tmp;
            }
            parent.set(rb, ra);
            size.set(ra, size.get(ra) + size.get(rb));
        }
    }

    const groups = new Set();
    for (const [x] of stones) {
        groups.add(find(x));
    }
    return stones.length - groups.size;
}

console.log(removeStones([[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]]));
