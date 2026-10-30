// O(n) time, O(n) space where n = words.length
function longestWord(words) {
    const uniqueWords = new Set(words);
    const byLength = {};
    for (const word of uniqueWords) {
        const len = word.length;
        if (!byLength[len]) byLength[len] = [];
        byLength[len].push(word);
    }
    const built = new Set([""]);
    let best = "";
    let length = 1;
    while (true) {
        const candidates = byLength[length] || [];
        const good = [];
        for (const w of candidates) {
            if (built.has(w.slice(0, -1))) {
                good.push(w);
            }
        }
        if (good.length === 0) {
            return best;
        }
        for (const w of good) {
            built.add(w);
        }
        let minWord = good[0];
        for (let i = 1; i < good.length; i++) {
            if (good[i] < minWord) minWord = good[i];
        }
        best = minWord;
        length++;
    }
}

console.log(longestWord(["w", "wo", "wor", "worl", "world"]));
