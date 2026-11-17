#include <bits/stdc++.h>
using namespace std;

// O(n * sigma) time (suffix automaton), O(n) space
long long longestRepeatedLength(string s) {
    vector<map<char, long long>> nxt(1);
    vector<long long> link(1, -1), length(1, 0), occ(1, 0);
    long long last = 0;
    for (char ch : s) {
        long long cur = nxt.size();
        nxt.push_back({});
        link.push_back(0);
        length.push_back(length[last] + 1);
        occ.push_back(1);
        long long p = last;
        while (p != -1 && !nxt[p].count(ch)) {
            nxt[p][ch] = cur;
            p = link[p];
        }
        if (p != -1) {
            long long q = nxt[p][ch];
            if (length[p] + 1 == length[q]) {
                link[cur] = q;
            } else {
                long long clone = nxt.size();
                map<char, long long> copied = nxt[q];
                nxt.push_back(copied);
                link.push_back(link[q]);
                length.push_back(length[p] + 1);
                occ.push_back(0);
                while (p != -1 && nxt[p].count(ch) && nxt[p][ch] == q) {
                    nxt[p][ch] = clone;
                    p = link[p];
                }
                link[q] = clone;
                link[cur] = clone;
            }
        }
        last = cur;
    }

    long long N = s.size();
    vector<vector<long long>> by_length(N + 1);
    for (long long v = 1; v < (long long)nxt.size(); v++) by_length[length[v]].push_back(v);
    long long best = 0;
    for (long long size = N; size >= 1; size--) {
        for (long long v : by_length[size]) {
            if (occ[v] >= 2) best = max(best, size);
            occ[link[v]] += occ[v];
        }
    }
    return best;
}

int main() {
    cout << longestRepeatedLength("banana") << endl;
    return 0;
}
