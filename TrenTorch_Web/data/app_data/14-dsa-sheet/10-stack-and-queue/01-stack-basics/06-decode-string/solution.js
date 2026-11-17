// O(n) time, O(n) space where n is length of decoded string
function decodeString(s) {
    const out = [];
    const openBlocks = [];
    let num = 0;
    for (const ch of s) {
        if (/\d/.test(ch)) {
            num = num * 10 + parseInt(ch, 10);
        } else if (ch === '[') {
            openBlocks.push([out.length, num]);
            num = 0;
        } else if (ch === ']') {
            const [start, count] = openBlocks.pop();
            if (count === 0) {
                out.length = start;
            } else if (count > 1) {
                const segment = out.slice(start);
                for (let i = 1; i < count; i++) {
                    out.push(...segment);
                }
            }
        } else {
            out.push(ch);
        }
    }
    return out.join('');
}

console.log(decodeString("3[a2[c]]"));
