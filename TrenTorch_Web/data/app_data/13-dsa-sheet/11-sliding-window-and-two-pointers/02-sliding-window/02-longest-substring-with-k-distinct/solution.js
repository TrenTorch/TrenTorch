// O(n) time, O(k) space
function longestKDistinct(s, k) {
    const count = new Map();
    let left = 0;
    let best = 0;
    for (let right = 0; right < s.length; right++) {
        const ch = s[right];
        count.set(ch, (count.get(ch) || 0) + 1);
        while (count.size > k) {
            const leftChar = s[left];
            const newCount = count.get(leftChar) - 1;
            if (newCount === 0) {
                count.delete(leftChar);
            } else {
                count.set(leftChar, newCount);
            }
            left++;
        }
        best = Math.max(best, right - left + 1);
    }
    return best;
}

console.log(longestKDistinct("eceba", 2));
