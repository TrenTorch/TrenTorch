// O(n) time, O(1) space
function calculate(s) {
    let total = 0;
    let last = 0;
    let num = 0;
    let op = '+';
    const str = s + '+';
    for (const ch of str) {
        if (ch >= '0' && ch <= '9') {
            num = num * 10 + (ch.charCodeAt(0) - 48);
        } else if (ch !== ' ') {
            if (op === '+') {
                total += last;
                last = num;
            } else if (op === '-') {
                total += last;
                last = -num;
            } else if (op === '*') {
                last *= num;
            } else { // op === '/'
                last = Math.trunc(last / num);
            }
            op = ch;
            num = 0;
        }
    }
    return total + last;
}

console.log(calculate("3+2*2"));
