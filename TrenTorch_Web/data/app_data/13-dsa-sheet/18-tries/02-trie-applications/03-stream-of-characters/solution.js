// O(|words| * max_len + |stream|) time, O(|words| * max_len) space
function streamChecker(words, stream) {
    const goto = [{}];
    const fail = [0];
    const ends = [false];

    for (const word of words) {
        let node = 0;
        for (const ch of word) {
            let child = goto[node][ch];
            if (child === undefined) {
                goto.push({});
                fail.push(0);
                ends.push(false);
                child = goto.length - 1;
                goto[node][ch] = child;
            }
            node = child;
        }
        ends[node] = true;
    }

    const queue = [];
    for (const child of Object.values(goto[0])) {
        queue.push(child);
    }

    while (queue.length > 0) {
        const node = queue.shift();
        if (ends[fail[node]]) {
            ends[node] = true;
        }
        for (const [ch, child] of Object.entries(goto[node])) {
            let f = fail[node];
            while (f && !(ch in goto[f])) {
                f = fail[f];
            }
            fail[child] = goto[f][ch] !== undefined ? goto[f][ch] : 0;
            queue.push(child);
        }
    }

    const out = [];
    let state = 0;
    for (const ch of stream) {
        while (state && !(ch in goto[state])) {
            state = fail[state];
        }
        state = goto[state][ch] !== undefined ? goto[state][ch] : 0;
        out.push(ends[state]);
    }
    return out;
}

console.log(streamChecker(["cd", "f", "kl"], "abcdefghijkl"));
