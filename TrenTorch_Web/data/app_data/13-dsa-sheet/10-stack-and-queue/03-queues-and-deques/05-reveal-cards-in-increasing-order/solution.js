// O(n log n) time, O(n) space
function revealCards(deck) {
    const n = deck.length;
    if (n === 0) return [];
    const result = new Array(n);
    const positions = new Array(n);
    for (let i = 0; i < n; i++) positions[i] = i;
    let head = 0;
    const sorted = [...deck].sort((a, b) => a - b);
    for (const card of sorted) {
        result[positions[head]] = card;
        head++;
        if (head < positions.length) {
            positions.push(positions[head]);
            head++;
        }
    }
    return result;
}

console.log(revealCards([17, 13, 11, 2, 3, 5, 7]));
