// O(n) time, O(1) space
function characterReplacement(s, k) {
    const count = {};
    let left = 0;
    let maxCount = 0;
    for (let right = 0; right < s.length; right++) {
        const ch = s[right];
        count[ch] = (count[ch] || 0) + 1;
        maxCount = Math.max(maxCount, count[ch]);
        if (right - left + 1 - maxCount > k) {
            count[s[left]]--;
            left++;
        }
    }
    return s.length - left;
}

console.log(characterReplacement("AABABBA", 1));
