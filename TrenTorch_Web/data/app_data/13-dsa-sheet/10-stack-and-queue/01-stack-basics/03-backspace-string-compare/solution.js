// O(n) time, O(1) space
function backspaceCompare(s, t) {
    function nextTyped(text, i) {
        let skip = 0;
        while (i >= 0) {
            if (text[i] === '#') {
                skip++;
            } else if (skip > 0) {
                skip--;
            } else {
                return i;
            }
            i--;
        }
        return -1;
    }

    let i = s.length - 1;
    let j = t.length - 1;
    while (true) {
        i = nextTyped(s, i);
        j = nextTyped(t, j);
        if (i < 0 && j < 0) {
            return true;
        }
        if (i < 0 || j < 0 || s[i] !== t[j]) {
            return false;
        }
        i--;
        j--;
    }
}

console.log(backspaceCompare("ab#c", "ad#c"));
