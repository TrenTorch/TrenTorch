// O(n) time, O(1) space (alphabet size bounded by 26)
function longestSubstringKRepeating(s, k) {
    function solve(lo, hi) {
        if (hi - lo < k) {
            return 0;
        }
        const counts = {};
        for (let i = lo; i < hi; i++) {
            const ch = s[i];
            counts[ch] = (counts[ch] || 0) + 1;
        }
        const rare = new Set();
        for (const [ch, c] of Object.entries(counts)) {
            if (c < k) {
                rare.add(ch);
            }
        }
        if (rare.size === 0) {
            return hi - lo;
        }
        let best = 0;
        let start = lo;
        for (let i = lo; i <= hi; i++) {
            if (i === hi || rare.has(s[i])) {
                best = Math.max(best, solve(start, i));
                start = i + 1;
            }
        }
        return best;
    }
    return solve(0, s.length);
}

console.log(longestSubstringKRepeating("aaabb", 3));
